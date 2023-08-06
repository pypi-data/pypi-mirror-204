# pylint: disable=no-name-in-module,import-error,too-few-public-methods,protected-access
"""
Configurable Argparse
=====================

Provides YAML config backed argument parsing to simplify
repetitive execution of python scripts expecting many arguments.

WARNING: the argument `--use_config` is reserved for the use of selecting a config YAML file (by default, configurable)
"""
import argparse
from pathlib import Path
from typing import Any, List, Optional, Union

from DRSlib.utils import assertTrue

import yaml

DEFAULT_USE_CONFIG_RESERVED_ARGUMENT = "--use_config"
CONFIG_NAME = lambda name: name.lower().replace(".yaml", "")
YAML_FILE = lambda base, name: base.with_suffix(f".{CONFIG_NAME(name)}.yaml")


class Argument:
    """Represents an argument to be added to an ArgumentParser"""

    def __init__(
        self, name: Union[List[str], str], kwargs: Optional[dict] = None
    ) -> None:
        self.names = [name] if isinstance(name, str) else name
        self.kwargs = kwargs if kwargs is not None else {}
        self.add_default_to_help()
        self.required = self.kwargs.pop("required", False)

    def add_default_to_help(self) -> None:
        """Adds representation of default value at the end of argument help message, if applicable."""
        # Case : no kwargs or no default => nothing to do
        if not self.kwargs or "default" not in self.kwargs:
            return
        _help = self.kwargs.get("help", "")
        # Case : default is already mentioned => don't add default
        if "default" in _help.lower():
            return
        _default = self.kwargs["default"]
        _default_repr = (
            " ".join(str(x) for x in _default)
            if isinstance(_default, list)
            else _default
        )
        _spacer = "" if len(_help) == 0 else " "
        self.kwargs["help"] = _help + _spacer + f"Default: {_default_repr}"

    def is_present_in_namespace(self, namespace: argparse.Namespace) -> bool:
        """Checks whether group is represented in namespace"""
        for name in self.names:
            if hasattr(namespace, name.lstrip("-")):
                return True
        return False

    def add_argument(
        self,
        parser: Union[argparse.ArgumentParser, argparse._MutuallyExclusiveGroup],
        reserved_name: str,
    ) -> None:
        """Add argument to parser"""
        assertTrue(
            not any(name == reserved_name for name in self.names),
            "Rejected argument for having the same name as reserved argument '{}'. Set `use_config_argument` to an unused argument name to avoid this.",
            reserved_name,
        )
        parser.add_argument(*self.names, **self.kwargs)


class ArgumentExclusiveGroup:
    """Represents an exclusive argument group to be added to an ArgumentParser"""

    def __init__(self, arguments: List[Argument], required: bool = False) -> None:
        self.args = arguments
        self.required = required

    def add_argument(self, parser: argparse.ArgumentParser, reserved_name: str) -> None:
        """Add argument group to parser"""
        group = parser.add_mutually_exclusive_group()
        for arg in self.args:
            arg.add_argument(group, reserved_name=reserved_name)

    def is_present_in_namespace(self, namespace: argparse.Namespace) -> bool:
        """Checks whether group is represented in namespace"""
        for arg in self.args:
            for name in arg.names:
                if hasattr(namespace, name.lstrip("-")):
                    return True
        return False

    @property
    def arguments(self) -> str:
        """Returns representation of arguments in group"""
        return " ".join(arg.names[-1] for arg in self.args)


def assert_type(expected: type, value: Any, name: str, blocking: bool = True) -> bool:
    """type asserting logic"""
    if blocking:
        assertTrue(
            isinstance(value, expected),
            "{}: expected a type, found a {type(value)} : '{value}'",
            name,
            type(value),
        )
    elif isinstance(value, expected):
        print(f"{name}: expected a {expected}, found a {type(value)} : '{value}'")
        return False
    return True


def nonNone(dictionnary: dict) -> dict:
    """Returns a dictionnary with same elements minus the ones with None values"""
    return {k: v for k, v in dictionnary.items() if v is not None}


def get_args(
    parser_args: dict,
    arguments: List[Argument],
    yaml_config_base: Path,
    use_config_argument: str = DEFAULT_USE_CONFIG_RESERVED_ARGUMENT,
) -> argparse.Namespace:
    """Parses CLI arguments, enforces required arguments

    `use_config_argument`: change if default value `--use_config` is an issue
    """
    assert_type(dict, parser_args, "parser_args")
    yaml_config_base = yaml_config_base.resolve()
    assertTrue(use_config_argument, "use_config_argument can't be None or empty !")

    # configure parser with given arguments
    parser = argparse.ArgumentParser(**parser_args)
    for arg in arguments:
        if not (
            assert_type(dict, Argument, "arg", blocking=False)
            or assert_type(dict, ArgumentExclusiveGroup, "arg", blocking=False)
        ):
            continue
        arg.add_argument(parser, reserved_name=use_config_argument)

    # Add `use_config` reserved argument
    parser.add_argument(
        use_config_argument,
        help="[configurable_argparse] Select YAML config file to load arguments from.",
    )

    # Parse arguments
    namespace: argparse.Namespace = parser.parse_args()

    # Config loading/saving
    use_config = use_config_argument.lstrip("-")
    cfg = getattr(namespace, use_config)
    delattr(namespace, use_config)
    if cfg:
        cfg_file = YAML_FILE(yaml_config_base, cfg)
        assertTrue(
            cfg_file.is_file(), "error: could not find config file '{}' !", cfg_file
        )
        config = yaml.safe_load(cfg_file.read_text(encoding="utf8"))
        assert_type(dict, config, "config")
        for k, v in config.items():
            setattr(namespace, k, v)

    # Ensure required arguments are present
    for arg in arguments:
        if arg.required:
            assertTrue(
                arg.is_present_in_namespace(namespace),
                "Error: one of the arguments {} is required. namespace={}",
                arg,
                namespace,
            )

    if not cfg:
        user_input = input(
            "Save arguments into YAML config file for later use (leave blank to skip) ? "
        )
        if user_input:
            cfg_file = YAML_FILE(yaml_config_base, user_input)
            with cfg_file.open("w", encoding="utf8") as f_cfg:
                yaml.dump(nonNone(vars(namespace)), f_cfg)
            print(f"Saved config {CONFIG_NAME(user_input)} (file '{cfg_file}')")

    return namespace


def main():
    """main, mostly an use example"""
    parser_args = {"prog": "Configurable Argparse", "description": __doc__}
    arguments = [
        Argument(name=("-t", "--test"), kwargs={"action": "store"}),
        ArgumentExclusiveGroup(
            [
                Argument(name="--debug", kwargs={"action": "store_true"}),
                Argument(name="--tesst", kwargs={"action": "store_true"}),
            ]
        ),
    ]
    yaml_cfg_base = Path(".").resolve() / "testconfig"
    print(get_args(parser_args, arguments, yaml_cfg_base))


if __name__ == "__main__":
    main()
