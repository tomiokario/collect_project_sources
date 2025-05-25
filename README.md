# collect_project_sources.py

`collect_project_sources.py` は、指定した拡張子のソースコードファイルをプロジェクトディレクトリ内から再帰的に収集し、Markdown 形式で 1 つのファイルにまとめて出力するツールです。

## 主な機能

* 任意の拡張子を指定して、その種類のファイルだけを対象に収集します。
* `.ignore` ファイルの内容に従って、無視するパスやパターンを指定できます。
* Git リポジトリ内で実行する場合は、`.gitignore` の設定も自動的に考慮されます。
* 各ファイルは Markdown のコードブロック（` ``` `）で囲まれ、ファイルパスを言語タグとして記載します。
* 出力された Markdown ファイルには、対象ソースの内容が順に記録されます。

## 使用方法

```bash
python collect_project_sources.py
```

## ️ 設定項目

スクリプト冒頭に以下の定数を設定することで、動作をカスタマイズできます。

| 定数名                 | 説明                       |
| ------------------- | ------------------------ |
| `TARGET_EXTENSIONS` | 収集対象の拡張子（例：`.py`, `.sh`） |
| `OUTPUT_FILE_NAME`  | 出力先となる Markdown ファイル名    |
| `IGNORE_FILE_NAME`  | 任意の無視パターンを記述したファイル名      |

例：

```python
TARGET_EXTENSIONS = {'.py', '.sh'}
OUTPUT_FILE_NAME = 'collected_sources.md'
IGNORE_FILE_NAME = '.ignore'
```

## `.ignore` ファイルについて

* `.ignore` ファイルには、無視したいファイルやディレクトリのパターンを 1 行ずつ記述します。
* `fnmatch`（Unix シェル形式）に基づくパターンマッチが行われます。
* 行頭が `#` の行はコメントとみなされます。

例（`.ignore`）：

```
# markdownを無視
*.md

# 特定ディレクトリを除外
tests/*
```

## 出力例（Markdown フォーマット）

出力ファイルには、以下のような Markdown 形式でファイル内容がまとめられます。

````markdown
```src/example.py
print("Hello, Python!")
```

```scripts/setup.sh
#!/bin/bash
echo "Setup complete"
```
````

## 動作条件

* Python 3.6 以降
* `.gitignore` の自動判定を使う場合は Git がインストールされていること

## 想定用途

* 複数ファイルで構成されたソースをLLMに渡したいとき
* コードレビュー用にプロジェクト全体を 1 ファイルにまとめたいとき
