## モジュールのパッケージ化

汎用性の高いモジュールを作成できたとき、パッケージに出来れば簡単にほかのpyファイルから実行することができる。

https://qiita.com/msi/items/d91ea3900373ff8b09d7

https://qiita.com/Tomato_otamoT/items/df01c754225aebc5a9da

pyproject.toml

pip install -e .

“__init__.py”

https://qiita.com/studio_haneya/items/9aad8f9ede11e58b41a8

https://qiita.com/gyu-don/items/833ceb2068f33a9a11e1

https://qiita.com/yaskitie/items/75eebf335d4fbb96551f

https://qiita.com/ezmscrap/items/1e66d67524228231da74

### 作成したパッケージのインストール方法
setup.pyと同じ階層で下記コマンド
```python
pip install -e .
```
### 自作パッケージのimport時にVSCodeで警告が出る場合
https://qiita.com/ezmscrap/items/1e66d67524228231da74
