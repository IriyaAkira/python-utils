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

import logging
import os
import shutil
import tempfile
import ctypes
from dirsync import sync
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def _is_hidden(path: Path) -> bool:
    """
    Determine whether the given file or directory is hidden.

    UNIX: Hidden if the name starts with a dot.
    Windows: Hidden if the name starts with a dot or the hidden file attribute is set.
    """
    if path.name.startswith('.'):
        return True
    if os.name == 'nt':
        try:
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
            if attrs == -1:
                return False
            FILE_ATTRIBUTE_HIDDEN = 0x2
            return bool(attrs & FILE_ATTRIBUTE_HIDDEN)
        except Exception:
            return False
    return False

def _ignore_hidden(dirpath, names):
    """
    `shutil.copytree` ignore callback that skips hidden files/directories.
    """
    ignore = set()
    base = Path(dirpath)
    for name in names:
        try:
            p = base / name
            if _is_hidden(p):
                logger.debug(f'Ignoring hidden item: {p}')
                ignore.add(name)
        except Exception as e:
            logger.debug(f'Error checking {name}: {e}')
            continue
    return ignore

def sync_dir(src: Path, dst: Path, exclude_hidden: bool = False, verbose: bool = True):
    """
    Perform directory synchronization.

    Synchronize differences from the source folder to the target folder.
    Files missing from the source will be removed from the target. The target
    directory will be created if it does not exist.

    Args:
        src (Path): Path to the source directory.
        dst (Path): Path to the destination directory.
        exclude_hidden (bool): If True, exclude hidden files and directories. Default: False.
        verbose (bool): Passed to `dirsync.sync` to control detailed output. Default: False.

    Raises:
        FileNotFoundError: If the source directory does not exist.
    """
    src = src.resolve()
    dst = dst.resolve()

    logger.debug('Checking if source directory exists')
    if not src.exists():
        logger.error(f"Source directory does not exist: {src}")
        raise FileNotFoundError(f"Source directory does not exist: {src}")

    logger.debug(f'Starting synchronization: {src} to {dst}')
    if exclude_hidden:
        # To exclude hidden items, copy the source to a temporary directory and sync from that copy
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_src = Path(tmpdir) / src.name
            logger.debug(f'Copying source to temporary dir (excluding hidden items): {temp_src}')
            shutil.copytree(src, temp_src, ignore=_ignore_hidden)
            logger.debug('Temporary copy completed; invoking dirsync.sync')
            sync(
                sourcedir=str(temp_src),
                targetdir=str(dst),
                action="sync",     # Incremental synchronization
                verbose=verbose,     # Display execution details
                purge=True,        # Delete files not in source directory
                create=True        # Auto-create target directory
            )
    else:
        sync(
            sourcedir=str(src),
            targetdir=str(dst),
            action="sync",     # Incremental synchronization
            verbose=verbose,     # Display execution details
            purge=True,        # Delete files not in source directory
            create=True        # Auto-create target directory
        )

    logger.debug(f'Synchronization completed: {src} to {dst}')

if __name__ == "__main__":
    """
    Main entry point.

    When executed directly, initialize the logging system and run synchronization
    for the configured directory.
    """
    # mylogger is only needed for direct execution; otherwise it interferes
    from myutilspkg import mylogger
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.basename(dir_path)
    mylogger.init_logger(file_name, dir_path)
    logger.debug('Direct execution detected')
    dir_src = os.path.dirname(os.path.abspath(__file__))
    dir_dst = Path.home() / 'mysyncdirdst'
    
    logger.debug('Starting synchronization')
    sync_dir(dir_src, dir_dst, exclude_hidden=True)
    logger.debug('Synchronization completed')
