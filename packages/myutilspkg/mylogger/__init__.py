# -*- coding: utf-8 -*-
"""
logger helper
----------------
ユーティリティ: アプリケーション／モジュール単位でログファイルを作成・初期化する補助関数群。

主な機能:
- `get_log_dir(dir_path=None)` : ログ格納ディレクトリを返す（未指定時はこのモジュールの配置ディレクトリを基準に 'log' を作成）。
- `get_log_file(file_name=None)` : ログファイル名を決定する。未指定時は呼び出し元のモジュール名から `<module>.log` を返す。
- `init_logger(module_name=None, dir_path=None)` : 指定されたディレクトリ／ファイル名で `logging` を初期化し、ファイル／コンソールハンドラを設定して `Logger` を返す。

使用例:
    # メインのモジュール上
    (import os)
    from logger import init_logger
    logger = init_logger()  # デフォルト: 当モジュールと同じ場所に ./log/(module).log を作る
    logger = init_logger(init_logger(os.path.splitext(os.path.basename(__file__))[0]))  # 当モジュールを使用した.pyファイルの名前でログファイルを生成する

    # 他のモジュール上（メインも含む）
    メインのモジュールから呼び出された別のモジュールでもloggingを下記のように使用できていれば当モジュールが活きる。
    from logging import getLogger
    logger = getLogger(__name__)
    logger.debug('log level debug')
    logger.info('log level info')
    logger.warning('log level warning')
    logger.error('log level error')

注意:
- `init_logger` は簡易的な初期化を行います。複数回呼ぶとハンドラが重複する可能性があるため、同一プロセス内での再初期化には注意してください。
参考:
- https://docs.python.org/ja/3.13/library/logging.html
- https://docs.python.org/ja/3.13/howto/logging.html
- https://docs.python.org/ja/3.13/howto/logging-cookbook.html
- https://qiita.com/amedama/items/b856b2f30c2f38665701
- https://qiita.com/ryoheiszk/items/362ae8ce344966b5516c
"""
from .main import init_logger
__all__ = ['init_logger']