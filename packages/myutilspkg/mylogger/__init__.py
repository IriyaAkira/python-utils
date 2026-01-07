# -*- coding: utf-8 -*-
"""
mylogger.main モジュール

このモジュールはアプリケーションやモジュール単位でのログ初期化を簡便に行うための補助関数を提供します。

提供関数:
- `init_logger(module_name=None, dir_path=None)` : ファイルハンドラ（ローテート）とコンソールハンドラを設定して `logging` を初期化し、`Logger` を返します。

注意事項:
- 同一プロセス内で `init_logger` を複数回呼ぶとハンドラが重複してログが重複出力されるため再初期化に注意してください。
- ログファイルは UTF-8 エンコーディングでローテーションが設定されています。

詳細な使用例はソースコード本体のコメントを参照してください。
"""
from .main import init_logger
__all__ = ['init_logger']