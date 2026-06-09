import py_compile
import os
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent

PYTHON_FILES = (
    BASE_DIR / "dict_utils.py",
    BASE_DIR / "excel_to_vndict.py",
    BASE_DIR / "vn_to_pinyin.py",
    BASE_DIR / "vn_to_telex.py",
    BASE_DIR / "validate_dicts.py",
    BASE_DIR / "web_ui.py",
)


def compile_scripts():
    print("檢查 Python 腳本語法...")
    for path in PYTHON_FILES:
        py_compile.compile(path, doraise=True)


def run_command(args, expect_success=True):
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    result = subprocess.run(
        args,
        cwd=REPO_ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
    )

    if expect_success and result.returncode != 0:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)

    if not expect_success and result.returncode == 0:
        command = " ".join(str(arg) for arg in args)
        raise SystemExit(f"命令應該失敗但成功了：{command}")

    if result.stdout and expect_success:
        print(result.stdout, end="")

    return result


def validate_dictionaries():
    print("驗證字典格式與根目錄同步狀態...")
    run_command([sys.executable, str(BASE_DIR / "validate_dicts.py")])


def validate_missing_word_list_guard():
    print("確認輔助腳本在缺少 WordList.txt 時不會覆寫輸出...")
    run_command([sys.executable, str(BASE_DIR / "vn_to_pinyin.py")], expect_success=False)
    run_command([sys.executable, str(BASE_DIR / "vn_to_telex.py")], expect_success=False)


def main():
    compile_scripts()
    validate_dictionaries()
    validate_missing_word_list_guard()
    print("驗證完成")


if __name__ == "__main__":
    main()
