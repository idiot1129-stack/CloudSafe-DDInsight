from pathlib import Path

from src.parser.file_scanner import FileScanner
from src.parser.capacity_parser import CapacityParser


class AutoSupportParser:
    def __init__(self, root: str):
        self.root = Path(root)

    def find_files(self) -> list[Path]:
        scanner = FileScanner(str(self.root))
        return scanner.scan()

    def parse_capacity_records(self):
        files = self.find_files()
        parser = CapacityParser()

        records = []
        for file in files:
            record = parser.parse(file)
            if record:
                records.append(record)

        return records