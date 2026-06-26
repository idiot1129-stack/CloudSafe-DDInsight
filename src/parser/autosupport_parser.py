from pathlib import Path

from src.parser.file_scanner import FileScanner


class AutoSupportParser:
    def __init__(self, root: str):
        self.root = Path(root)

    def find_files(self) -> list[Path]:
        scanner = FileScanner(str(self.root))
        return scanner.scan()