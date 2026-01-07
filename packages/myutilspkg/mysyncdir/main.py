# -*- coding: utf-8 -*-
"""
mysyncdir.main モジュール

ディレクトリ同期を行う簡易ユーティリティを提供します。

主な機能:
- `sync_dir(src, dst, exclude_hidden=False, verbose=False)`:
    - `dirsync.sync` を用いて差分（増分）同期を実行します。
    - 同期元に存在しないファイルは同期先から削除されます（`purge=True`）。
    - 同期先が存在しない場合は自動で作成されます（`create=True`）。
    - `exclude_hidden=True` の場合、隠しファイル・隠しフォルダを除外するため、一時ディレクトリへコピーしてから同期を実行します。
    - `verbose` 引数は内部の `dirsync.sync` に渡され、詳細出力の有無を制御します。

内部ヘルパー:
- `_is_hidden(path: Path)` : UNIX/Windows の判定方法に基づき隠しファイル/フォルダかどうかを判定します。
- `_ignore_hidden(dirpath, names)` : `shutil.copytree` の ignore コールバックとして隠し項目を除外します。

注意事項:
- Windows の隠し属性判定に `ctypes` を使用しています。
- 直接実行すると `myutilspkg.mylogger.init_logger` を呼んでログを初期化し、ホーム配下の `mysyncdirdst` に同期を実行します。
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
    ファイル/フォルダが隠しファイルかどうかを判定する。
    
    UNIX系: ファイル名が . で始まるかで判定
    Windows: ファイル名が . で始まる、または隠し属性を持つかで判定
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
    shutil.copytree の ignore コールバック。隠しファイル/フォルダをスキップする。
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
    ディレクトリ同期を実行する関数。
    
    同期元フォルダから同期先フォルダへの差分同期を行う。
    同期元に存在しないファイルは同期先から削除され、
    同期先フォルダが存在しない場合は自動作成される。
    
    Args:
        src (Path): 同期元フォルダのパス
        dst (Path): 同期先フォルダのパス
        exclude_hidden (bool): True の場合、隠しファイル・隠しフォルダを除外する。デフォルト: False
        verbose (bool): `dirsync.sync` に渡す詳細出力フラグ。True にすると処理詳細が出力されます。デフォルト: False
        
    Raises:
        FileNotFoundError: 同期元フォルダが存在しない場合
    """
    src = src.resolve()
    dst = dst.resolve()

    logger.debug('Checking if source directory exists')
    if not src.exists():
        logger.error(f"Source directory does not exist: {src}")
        raise FileNotFoundError(f"Source directory does not exist: {src}")

    logger.debug(f'Starting synchronization: {src} to {dst}')
    if exclude_hidden:
        # 隠しファイルを除外するため、一時ディレクトリへコピーしてから同期する
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
    メインエントリーポイント。
    
    このスクリプトが直接実行された場合、ログシステムを初期化して
    指定されたディレクトリの同期を実行する。
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
