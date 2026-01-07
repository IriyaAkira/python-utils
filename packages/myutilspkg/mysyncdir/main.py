# -*- coding: utf-8 -*-

import logging
import os
from dirsync import sync
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def sync_dir(src: Path, dst: Path):
    """
    ディレクトリ同期を実行する関数。
    
    同期元フォルダから同期先フォルダへの差分同期を行う。
    同期元に存在しないファイルは同期先から削除され、
    同期先フォルダが存在しない場合は自動作成される。
    
    Args:
        src (Path): 同期元フォルダのパス
        dst (Path): 同期先フォルダのパス
        
    Raises:
        FileNotFoundError: 同期元フォルダが存在しない場合
    """
    src = src.resolve()
    dst = dst.resolve()

    logger.debug('Checking if source directory exists')
    if not src.exists():
        logger.error(f"Source directory does not exist: {src}")
        raise FileNotFoundError(f"Source directory does not exist: {src}")

    # Perform incremental sync (deletions are also reflected)
    logger.debug(f'Starting synchronization: {src} to {dst}')
    sync(
        sourcedir=str(src),
        targetdir=str(dst),
        action="sync",     # Incremental synchronization
        verbose=True,      # Display execution details
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
    sync_dir(dir_src, dir_dst)
    logger.debug('Synchronization completed')
