from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".log",
    ".xml",
    ".json",
}

SUPPORTED_NAMES = {
    "autosupport",
}


def is_supported_file(file: Path) -> bool:
    name = file.name.lower()

    if file.suffix.lower() in SUPPORTED_EXTENSIONS:
        return True

    if name == "autosupport":
        return True

    if name.startswith("autosupport."):
        return True

    return False


class FileScanner:
    def __init__(self, input_path: str):
        self.input_path = Path(input_path)

    def scan(self) -> list[Path]:
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input path not found: {self.input_path}")

        files: list[Path] = []

        if self.input_path.is_file():
            if is_supported_file(self.input_path):
                files.append(self.input_path)
            return sorted(files)

        for file in self.input_path.rglob("*"):
            if file.is_file() and is_supported_file(file):
                files.append(file)

        return sorted(files)