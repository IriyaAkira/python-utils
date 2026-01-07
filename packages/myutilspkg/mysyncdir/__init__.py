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
from .main import sync_dir
__all__ = ['sync_dir']