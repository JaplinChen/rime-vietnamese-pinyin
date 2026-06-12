import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from dict_utils import ROOT_DIR
from web_ui import import_terms


DEFAULT_SOURCE = Path(r"D:\Works\TypeTwo\package\glossary.json")


def parse_args():
    parser = argparse.ArgumentParser(description="從 TypeTwo 詞彙表補充 VietnameseWordList.xlsx。")
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help=f"TypeTwo glossary JSON 路徑，預設：{DEFAULT_SOURCE}",
    )
    parser.add_argument(
        "--mode",
        choices=("merge", "replace"),
        default="merge",
        help="merge 只補中文空白欄與新增詞條；replace 會先清空中文欄再套用匯入內容。",
    )
    parser.add_argument(
        "--sync-root",
        action="store_true",
        help="匯入後同步更新專案根目錄的 vn.dict.yaml 與 vn_han.dict.yaml。",
    )
    return parser.parse_args()


def run_generate(sync_root):
    args = [sys.executable, str(Path(__file__).resolve().parent / "excel_to_vndict.py")]
    if sync_root:
        args.append("--sync-root")
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(
        args,
        cwd=ROOT_DIR,
        env=env,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(result.stdout, end="")
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main():
    args = parse_args()
    if not args.source.exists():
        raise SystemExit(f"找不到 TypeTwo 詞彙表：{args.source}")

    text = args.source.read_text(encoding="utf-8")
    decoded = json.loads(text)
    if not isinstance(decoded, dict) or not decoded:
        raise SystemExit("TypeTwo 詞彙表必須是非空 JSON 物件")

    result = import_terms({"format": "json", "mode": args.mode, "text": text})
    print(f"來源：{args.source}")
    print(f"模式：{result['mode']}")
    print(f"匯入：{result['imported']} 筆")
    print(f"新增：{result['appended']} 筆")
    print(f"更新：{result['updated']} 筆")
    print(f"略過：{result['skipped']} 行")
    print(f"備份：{result['backup']}")

    run_generate(args.sync_root)


if __name__ == "__main__":
    main()
