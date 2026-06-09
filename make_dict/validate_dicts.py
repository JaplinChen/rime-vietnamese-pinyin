import argparse
from collections import Counter
from pathlib import Path

from dict_utils import BASE_DIR, ROOT_DIR


DICT_FILES = (
    ("vn", ROOT_DIR / "vn.dict.yaml", BASE_DIR / "vn.dict.yaml"),
    ("vn_han", ROOT_DIR / "vn_han.dict.yaml", BASE_DIR / "vn_han.dict.yaml"),
)


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def split_dict(text):
    lines = text.splitlines()
    try:
        body_start = lines.index("...") + 1
    except ValueError as exc:
        raise ValueError("找不到字典表頭結束標記 `...`") from exc

    return lines[:body_start], [line for line in lines[body_start:] if line.strip()]


def validate_header(name, header):
    expected = f"name: {name}"
    if expected not in header:
        raise ValueError(f"表頭缺少 `{expected}`")

    if "# encoding: utf-8" not in header:
        raise ValueError("表頭缺少 UTF-8 宣告")


def validate_entries(entries):
    invalid = []
    for line_number, line in enumerate(entries, start=1):
        columns = line.split("\t")
        if len(columns) != 3:
            invalid.append((line_number, line))
            continue

        word, code, weight = columns
        if not word.strip() or not code.strip() or not weight.isdigit():
            invalid.append((line_number, line))

    if invalid:
        preview = "; ".join(f"{line_number}: {line}" for line_number, line in invalid[:5])
        raise ValueError(f"發現 {len(invalid)} 筆格式錯誤：{preview}")


def duplicate_preview(entries, limit=5):
    duplicates = []
    for line, count in Counter(entries).items():
        if count > 1:
            duplicates.append((line, count))

    return duplicates[:limit], len(duplicates)


def validate_pair(name, root_path, generated_path):
    root_text = read_text(root_path)
    generated_text = read_text(generated_path)

    if root_text != generated_text:
        raise ValueError(f"{root_path.name} 與 make_dict 內產物不一致")

    header, entries = split_dict(generated_text)
    validate_header(name, header)
    validate_entries(entries)

    duplicates, duplicate_count = duplicate_preview(entries)
    return len(entries), duplicate_count, duplicates


def parse_args():
    parser = argparse.ArgumentParser(description="驗證 Rime 越南語字典產物。")
    parser.add_argument(
        "--strict-duplicates",
        action="store_true",
        help="發現完全重複行時視為驗證失敗。",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    duplicate_failures = []

    for name, root_path, generated_path in DICT_FILES:
        entry_count, duplicate_count, duplicates = validate_pair(name, root_path, generated_path)
        print(f"{name}: {entry_count} 筆，重複行 {duplicate_count} 組")
        for line, count in duplicates:
            print(f"  重複 {count} 次：{line}")
        if duplicate_count:
            duplicate_failures.append((name, duplicate_count))

    if args.strict_duplicates and duplicate_failures:
        summary = "，".join(f"{name} {count} 組" for name, count in duplicate_failures)
        raise SystemExit(f"重複行驗證失敗：{summary}")

    print("字典驗證完成")


if __name__ == "__main__":
    main()
