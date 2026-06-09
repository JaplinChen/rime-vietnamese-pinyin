from pathlib import Path
import tempfile
import warnings

warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API.*",
    category=UserWarning,
    module="ftfy.chardata",
)
import visen


BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent


def clean_tone(text):
    return visen.clean_tone(text)


def remove_tone(text):
    return visen.remove_tone(text)


def to_telex(text):
    codes = []
    for word in text.split():
        # visen 會把「ươ」輸出為「uwow」，目前字典沿用「uow」。
        codes.append(visen.get_enter_code(word).replace("uwow", "uow"))
    return " ".join(codes).replace("\n", "").replace("\r", "").strip()


def write_text_atomic(path, text):
    path = Path(path)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        newline="\r\n",
        delete=False,
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    ) as temp_file:
        temp_path = Path(temp_file.name)
        temp_file.write(text)
    temp_path.replace(path)


def copy_text_atomic(source_path, target_path):
    source_path = Path(source_path)
    target_path = Path(target_path)
    write_text_atomic(target_path, source_path.read_text(encoding="utf-8"))
