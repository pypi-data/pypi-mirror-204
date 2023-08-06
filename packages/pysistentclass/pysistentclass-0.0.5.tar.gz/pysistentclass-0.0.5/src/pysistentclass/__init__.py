from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass, field, make_dataclass
from enum import Enum
from typing import Dict, List, Union, Any, Type

from importlib import import_module

import json
import yaml
import toml

import inspect
import hashlib

import colorlog
import logging


def logger(name: str) -> logging.Logger:
    logger = colorlog.getLogger(name)
    myFormatter = colorlog.ColoredFormatter(log_colors={
        'DEBUG': 'cyan', 'INFO': 'reset', 'ERROR': 'bold_red', 'WARNING': 'yellow'}, fmt="%(log_color)s%(levelname)s %(asctime)s " + name + " > %(message)s")
    handler = colorlog.StreamHandler()
    handler.setFormatter(myFormatter)
    logger.addHandler(handler)

    return logger


LOGGER = logger(__name__ + ".py")


class SettingsAttributeError(Exception):
    pass


def skip_underscore_keys(obj): return {
    k: v for k, v in vars(obj).items() if not k.startswith("_")
}


def json_pretty(obj): return json.dumps(
    obj, indent=4, sort_keys=True, default=vars)


class Format(str, Enum):
    deserializer: callable
    serializer: callable

    def __new__(
        cls, name: str, deserializer: callable = None, serializer: callable = None
    ) -> Format:
        obj = str.__new__(cls, name)
        obj._value_ = name
        obj.deserializer = deserializer
        obj.serializer = serializer
        return obj

    JSON = (
        "json",
        lambda s, object_hook: json.loads(s, object_hook=object_hook),
        lambda obj: json.dumps(obj, indent=4, sort_keys=True, default=vars),
    )
    YAML = ("yaml", yaml.safe_load, yaml.safe_dump)
    TOML = ("toml", toml.loads, toml.dumps)


class Scope(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"

    class _ScopeRepr:
        def __repr__(self) -> str:
            pass


def pysistentclass(cls=None, /, *, init=True) -> Type[_T@dataclass]:
    """
    pysistentclass decorator

    This decorator can be used to mark a class as a pysistentclass.
    """
    # return make_dataclass(cls.__name__)
    datacls = dataclass(cls)
    setattr(datacls, "_scope", getattr(datacls, "_scope", Scope.PUBLIC))
    setattr(datacls, "_class_key", None)
    return datacls


@dataclass
class Settings(dict):
    """ Settings class

    This is a dataclass that holds the settings for the application. It
    is a subclass of dict, so it can be used as a dict.

    It can be used in two ways:

    1. If you don't need to store any data in your settings, you can use
    it as a singleton, by passing the __file__ attribute of the module
    that is using it as a parameter. It will automatically load the
    settings from the settings directory that is in the same directory
    as the module.

    2. If you need to store data in your settings, you can create a
    subclass of Settings and add data fields to it. In that case, you
    need to pass a settings_dir parameter to the constructor. This
    parameter should be the path to the directory where the settings
    file will be stored.
    """
    settings_dir: Union[Path, str]

    _classes: Dict[str, Dict[str, str]] = field(
        default_factory=dict, init=False)
    _settings: Dict[str, object] = field(default_factory=dict, init=False)

    module_names: List[str] = field(default_factory=list)
    format: Format = Format.JSON
    logging_level: int = logging.DEBUG

    def json_object_hook(self, obj: dict) -> object:
        if "_class_key" in obj:
            class_key = obj["_class_key"]
            module = import_module(self._classes[class_key]["module"])
            class_name = self._classes[class_key]["class_name"]
            if not hasattr(module, class_name):
                raise SettingsAttributeError(
                    f"{module} does not have {class_name}")
            class_obj = getattr(module, class_name)
            return class_obj(**obj)
        return obj

    def __post_init__(self):
        LOGGER.setLevel(self.logging_level)
        LOGGER.debug(f"__post_init__()")
        LOGGER.debug(f"registering classes")
        self.settings_dir = Path(self.settings_dir)
        if not self.settings_dir.is_dir():
            self.settings_dir = self.settings_dir.parent
        self.settings_file = self.settings_dir / "settings"
        class_keys_file = self.settings_file.parent / "classes.json"
        if not class_keys_file.exists():
            LOGGER.debug(f"creating {class_keys_file}")
            class_keys_file.write_text("{}")
        self._classes = json.loads(class_keys_file.read_text())

        if (nmodules := len(self.module_names)) == 0:
            LOGGER.warn("no modules specified")
        else:
            LOGGER.debug(
                f"importing {len(self.module_names)} modules: {', '.join(self.module_names)}"
            )
        for mod_name in self.module_names:
            try:
                module = import_module(mod_name)
            except ModuleNotFoundError as e:
                LOGGER.error(f"module '{mod_name}' not found")
                exit(1)
            classes = inspect.getmembers(
                module,
                lambda o: inspect.isclass(o)
                and hasattr(o, "_class_key")
                and hasattr(o, "_scope"),
            )
            for class_name, class_obj in classes:
                key = f"{mod_name}.{class_name}"
                key_hash = hashlib.md5(key.encode()).hexdigest()
                if key_hash in self._classes:
                    LOGGER.debug(f"o {key}")
                else:
                    LOGGER.debug(f"+ {key}")
                    self._classes[key_hash] = {
                        "module": mod_name,
                        "class_name": class_name,
                    }
        class_keys_file.write_text(json.dumps(self._classes, indent=4))
        if not self.settings_file.is_file():
            if self.settings_file.suffix == "":
                self.settings_file = self.settings_file.with_suffix(
                    f".{self.format.value}"
                )
            self.settings_file.touch()
        LOGGER.debug(f"defining settings")
        LOGGER.debug(f"format={self.format}")
        for class_key, module_class_dict in self._classes.items():
            module = import_module(module_class_dict["module"])
            class_obj = getattr(module, module_class_dict["class_name"])
            scope = getattr(class_obj, "_scope", Scope.PUBLIC)
            instance = class_obj(
                _class_key=class_key,
                _scope=scope,
            )
            LOGGER.debug(f"+ instance of {class_obj}")
            self._settings[module_class_dict["class_name"]] = instance

    def get(self, key: str) -> Any:
        return self._settings[key]

    def write(self):
        serialized = self.format.serializer(self._settings)
        self.settings_file.write_text(serialized)

    def read(self):
        LOGGER.debug(f"reading settings {self.settings_file}")
        serialized = self.settings_file.read_text()
        default_serialized = self.format.serializer(self._settings)
        deserialized = {}
        try:
            if serialized:
                deserialized = self.format.deserializer(
                    serialized, self.json_object_hook
                )
        except SettingsAttributeError as e:
            LOGGER.debug(e)
        if serialized != default_serialized:
            LOGGER.debug("serialized != default_serialized")
        if not deserialized:
            LOGGER.debug(
                "deserialized is None or empty using default settings!")
            deserialized = self._settings
        self._settings = deserialized
        self.public = {}
        self.private = {}
        for k, v in self._settings.items():
            if v._scope == Scope.PUBLIC:
                self.public[k] = v
            else:
                self.private[k] = v

    def __repr__(self) -> str:
        return json.dumps(
            self._settings, sort_keys=True, default=skip_underscore_keys, indent=4
        )
