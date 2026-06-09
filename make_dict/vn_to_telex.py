from dict_utils import BASE_DIR, clean_tone, to_telex, write_text_atomic


SOURCE_PATH = BASE_DIR / "WordList.txt"
OUTPUT_PATH = BASE_DIR / "vn_telex.txt"


def main():
    if not SOURCE_PATH.exists():
        raise SystemExit(f"找不到來源檔：{SOURCE_PATH}")

    lines = []
    with SOURCE_PATH.open("r", encoding="utf-8") as source_file:
        for source_text in source_file:
            clean_text = clean_tone(source_text).strip()
            telex_text = to_telex(clean_text)
            lines.append(f"{clean_text}\t{telex_text}\t20000\n")

    write_text_atomic(OUTPUT_PATH, "".join(lines))


if __name__ == "__main__":
    main()
