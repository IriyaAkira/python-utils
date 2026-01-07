# -*- coding: utf-8 -*-
"""
mysyncdir.main module

Simple utility for directory synchronization.

Main features:
- `sync_dir(src, dst, exclude_hidden=False, verbose=False)`:
    - Performs incremental synchronization using `dirsync.sync`.
    - Removes files in the target that are not present in the source (`purge=True`).
    - Creates the target directory if it does not exist (`create=True`).
    - If `exclude_hidden=True`, copies the source to a temporary directory excluding hidden files and directories, then synchronizes from that copy.
    - The `verbose` argument is passed to `dirsync.sync` to control detailed output.

Helpers:
- `_is_hidden(path: Path)`: Determine whether a file or directory is hidden using UNIX/Windows rules.
- `_ignore_hidden(dirpath, names)`: `shutil.copytree` ignore callback that excludes hidden items.

Notes:
- Uses `ctypes` to check the Windows hidden attribute.
- When run directly, initializes logging via `myutilspkg.mylogger.init_logger` and synchronizes to `mysyncdirdst` under the user's home directory.
"""
from .main import sync_dir
__all__ = ['sync_dir']