# -*- coding: utf-8 -*-
"""
mysyncdir.main モジュール

このモジュールはディレクトリ同期用の簡易ユーティリティを提供します。

主な機能:
- `sync_dir(src, dst, exclude_hidden=False)`: 同期元フォルダから同期先フォルダへ差分同期（削除を含む）を実行します。
  `exclude_hidden=True` の場合、src側の隠しファイル・隠しフォルダは同期対象外です。

直接実行した場合はロガーを初期化し、スクリプトのディレクトリを
ホームディレクトリ配下の `mysyncdirdst` に同期します。

内部で `dirsync.sync` を利用します。
"""
from .main import sync_dir
__all__ = ['sync_dir']