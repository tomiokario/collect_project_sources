#!/usr/bin/env python3
import subprocess
import fnmatch
import sys
from pathlib import Path

# ===== ユーザーが指定する設定 =====
TARGET_EXTENSIONS = {'.py', '.sh'}           # 収集対象の拡張子
OUTPUT_FILE_NAME   = 'combined.txt'          # 出力ファイル名
IGNORE_FILE_NAME   = '.ignore'               # .ignore ファイル名

base_path = Path('.')                        # 検索開始ディレクトリ

# .ignore からパターンを読み込む
ignore_patterns = []
ignore_file = base_path / IGNORE_FILE_NAME
if ignore_file.exists():
    try:
        ignore_patterns = [
            line.strip()
            for line in ignore_file.read_text(encoding='utf-8').splitlines()
            if line.strip() and not line.startswith('#')
        ]
    except Exception as e:
        print(f"警告: '{IGNORE_FILE_NAME}' の読み込みに失敗しました: {e}")

def is_ignored_path(relative_path: Path) -> bool:
    """.ignore のパターンまたは .gitignore で無視対象か判定"""
    path_str = str(relative_path)
    if any(fnmatch.fnmatch(path_str, pattern) for pattern in ignore_patterns):
        return True
    try:
        result = subprocess.run(
            ['git', 'check-ignore', '--quiet', path_str],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception:
        return False

# 拡張子が未設定の場合は警告して終了
if not TARGET_EXTENSIONS:
    print("拡張子が指定されていません。スクリプト内の TARGET_EXTENSIONS を設定してください。")
    sys.exit(0)

# 対象ファイルを再帰的に収集
matched_files = [
    file_path
    for file_path in base_path.rglob('*')
    if file_path.suffix in TARGET_EXTENSIONS
       and file_path.name != OUTPUT_FILE_NAME
       and not is_ignored_path(file_path.relative_to(base_path))
]

if not matched_files:
    print(f"指定された拡張子のファイルが見つかりませんでした: {', '.join(sorted(TARGET_EXTENSIONS))}")
    sys.exit(0)

matched_files.sort()

# Markdown形式で書き出し
try:
    with open(OUTPUT_FILE_NAME, 'w', encoding='utf-8') as output_file:
        for file_path in matched_files:
            relative = file_path.relative_to(base_path)
            output_file.write(f"```{relative}\n")
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                output_file.write(content)
            except Exception as e:
                print(f"警告: ファイル '{relative}' を読み込めませんでした: {e}")
            output_file.write("```\n\n")
    print(f"{len(matched_files)} 件のファイルを '{OUTPUT_FILE_NAME}' に統合しました。対象拡張子: {', '.join(sorted(TARGET_EXTENSIONS))}")
except Exception as e:
    print(f"出力ファイル '{OUTPUT_FILE_NAME}' の書き込み中にエラーが発生しました: {e}", file=sys.stderr)
    sys.exit(1)
