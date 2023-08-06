"""The `configs` package contains modules:
    * `config`: the base configuration object containing attributes for options
        which either do not apply to any package in particular or else apply to
        multiple packages
    * `helpers`: contains functions for building configuration objects and
        parsing command-line arguments
"""
from .config import BaseConfig
from .helpers import build_config


__all__ = (
    "BaseConfig",
    "build_config",
)
