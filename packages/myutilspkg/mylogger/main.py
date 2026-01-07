# -*- coding: utf-8 -*-
"""
mylogger.main モジュール

アプリケーションやモジュール単位でログ初期化を簡便に行うための補助関数を提供します。

提供関数:
- `get_log_dir(dir_path=None)` : ログ保存用ディレクトリの絶対パスを返します。未指定時は本モジュール配置ディレクトリ内に `log` サブディレクトリを作成します。
- `get_log_file(file_name=None)` : ログファイル名を決定します。未指定時はモジュール名または実行ファイル名に基づく `<name>.log` を返します。
- `init_logger(module_name=None, dir_path=None, backup_count: int = 5)` : ルートロガーにファイルハンドラ（ローテート）とコンソールハンドラを追加して初期化し、`logging.Logger` を返します。`backup_count` でローテート時に保持するバックアップ世代数を指定できます（デフォルト: 5）。ログは UTF-8 エンコーディングで出力されます。

注意事項:
- 同一プロセス内で `init_logger` を複数回呼ぶとハンドラが重複してログが二重出力されるため、再初期化には注意してください。
"""
from pathlib import Path
import logging
import logging.handlers
import os

def get_log_dir(dir_path=None):
    """Return a directory path for storing logs.

    If `dir_path` is provided it will be used as the base directory (absolute path).
    If `dir_path` is None the directory containing this module is used as base and
    a `log` subdirectory is created there.

    Returns
    -------
    str
        Absolute path to the log directory (created if necessary).
    """
    if dir_path is None:
        # Use the directory where this module resides
        base_dir = Path(__file__).resolve().parent
    else:
        # Normalize provided path to an absolute path
        base_dir = Path(os.path.abspath(dir_path))

    log_dir = base_dir / 'log'
    log_dir.mkdir(parents=True, exist_ok=True)
    return str(log_dir)

def get_log_file(file_name=None):
    """Return the log file name to use.

    If ``file_name`` is provided, it is returned as-is. When ``file_name`` is
    ``None``, the function derives a filename from the module context:
    - If this module is imported, ``__name__`` is used as the base name.
    - If this module is executed directly (``__name__ == '__main__'``), the
      stem of this file (filename without extension) is used instead.

    The returned value is a simple filename (e.g. ``"my_module.log"``).

    Parameters
    ----------
    file_name : str | None
        Explicit filename to use. If ``None``, derive the filename from the
        module name as described above.

    Returns
    -------
    str
        Log filename (without directory path).
    """
    if file_name is None:
        if __name__ == '__main__':
            module_name = os.path.splitext(os.path.basename(__file__))[0]
        else:
            module_name = __name__
    else:
        module_name = file_name

    return f"{module_name}.log"

def init_logger(module_name=None, dir_path=None, backup_count: int = 5): 
    """Initialize logging and return a configured logger.

    Parameters
    ----------
    module_name : str | None
        If provided, used as the base name of the log file (without extension).
        If None the caller's module name (or this module's name when run directly)
        will be used by `get_log_file`.
    dir_path : str | None
        Base directory where the `log` subdirectory will be created. If None,
        the directory containing this module is used.
    backup_count : int
        Number of rotated backup files to keep (passed to the file handler).
        Defaults to 5.

    Returns
    -------
    logging.Logger
        The configured root logger (note: this function attaches handlers to the
        root logger). Be careful to avoid calling this multiple times in the same
        process to prevent duplicate handlers.
    """
    # Determine log directory and file path
    log_dir = get_log_dir(dir_path)
    log_name = get_log_file(module_name)
    log_file_path = os.path.join(log_dir, log_name)

    # Configure the root logger so that all module loggers propagate to it
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # File handler: rotating file with UTF-8 encoding
    fh = logging.handlers.RotatingFileHandler(
        log_file_path,
        maxBytes=1024 * 1024,
        backupCount=backup_count,
        encoding="utf-8",
    )
    fh.setLevel(logging.DEBUG)

    # Console handler (stderr) for immediate visibility
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Common formatter applied to both handlers
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d, %(levelname)s, %(name)s, %(funcName)s, %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Attach handlers to the root logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

if __name__ == '__main__':
    logger = init_logger()
    logger.debug('log level debug')
    logger.info('log level info')
    logger.warning('log level warning')
    logger.error('log level error')
