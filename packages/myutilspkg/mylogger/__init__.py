# -*- coding: utf-8 -*-
"""
mylogger.main module

Utilities to simplify initializing logging for applications or modules.

Provides:
- `init_logger(module_name=None, dir_path=None, backup_count: int = 5)`: Initialize the root logger with a rotating file handler and a console handler and return a `logging.Logger`. Use `backup_count` to control how many rotated backups are kept (default: 5). Logs are written using UTF-8 encoding.

Notes:
- Calling `init_logger` multiple times in the same process will add duplicate handlers and can produce duplicate log output.
"""
from .main import init_logger
__all__ = ['init_logger']