from dict_utils import BASE_DIR, clean_tone, remove_tone, write_text_atomic


SOURCE_PATH = BASE_DIR / "WordList.txt"
OUTPUT_PATH = BASE_DIR / "vn_pinyin.txt"


def main():
    if not SOURCE_PATH.exists():
        raise SystemExit(f"找不到來源檔：{SOURCE_PATH}")

    lines = []
    with SOURCE_PATH.open("r", encoding="utf-8") as source_file:
        for source_text in source_file:
            clean_text = clean_tone(source_text).strip()
            no_tone_text = remove_tone(clean_text).strip()
            lines.append(f"{clean_text}\t{no_tone_text}\t30000\n")

    write_text_atomic(OUTPUT_PATH, "".join(lines))


if __name__ == "__main__":
    main()
