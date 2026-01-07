# -*- coding: utf-8 -*-
"""
mylogger.main モジュール

アプリケーションやモジュール単位でログ初期化を簡便に行うための補助関数を提供します。

提供関数:
- `init_logger(module_name=None, dir_path=None, backup_count: int = 5)` : ルートロガーにファイルハンドラ（ローテート）とコンソールハンドラを追加して初期化し、`logging.Logger` を返します。`backup_count` でローテート時に保持するバックアップ世代数を指定できます（デフォルト: 5）。ログは UTF-8 エンコーディングで出力されます。

注意事項:
- 同一プロセス内で `init_logger` を複数回呼ぶとハンドラが重複してログが二重出力されるため、再初期化には注意してください。
"""
from .main import init_logger
__all__ = ['init_logger']