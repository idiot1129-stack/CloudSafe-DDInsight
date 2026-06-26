from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QFileDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QCheckBox, QProgressBar, QMessageBox, QGroupBox,
)

from src.parser.autosupport_parser import AutoSupportParser


APP_NAME = "CloudSafe DD Insight Professional"
APP_VERSION = "2.1"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(980, 720)
        self._build_ui()

    def _build_ui(self):
        root = QWidget()
        main = QVBoxLayout(root)
        main.setContentsMargins(0, 0, 0, 0)

        header = QLabel(
            f"<h1>{APP_NAME}</h1>"
            f"<p>Version {APP_VERSION}　|　Enterprise Data Domain Capacity & Health Analyzer</p>"
        )
        header.setStyleSheet("""
            QLabel {
                background-color: #173B63;
                color: white;
                padding: 24px;
            }
            h1 {
                font-size: 30px;
                margin: 0;
            }
            p {
                font-size: 13px;
                margin-top: 8px;
            }
        """)
        main.addWidget(header)

        body = QVBoxLayout()
        body.setContentsMargins(28, 28, 28, 18)
        body.setSpacing(18)

        self.input_path = QLineEdit()
        self.output_path = QLineEdit(str(Path.cwd() / "output" / "DD_Insight_Report.xlsx"))
        self.company_name = QLineEdit("CloudSafe Technologies")

        body.addLayout(self._path_row("AutoSupport Folder / ZIP / File", self.input_path, self.browse_input))
        body.addLayout(self._path_row("Output Excel", self.output_path, self.browse_output))

        body.addWidget(QLabel("Company Name"))
        body.addWidget(self.company_name)

        group = QGroupBox("Report Content")
        grid = QGridLayout(group)

        self.checks = {}
        items = [
            "Dashboard", "Summary", "Detail", "Usage Trend",
            "Growth Trend", "Compression Trend", "Daily Ingest", "Forecast"
        ]

        for i, name in enumerate(items):
            cb = QCheckBox(name)
            cb.setChecked(True)
            self.checks[name] = cb
            grid.addWidget(cb, i // 4, i % 4)

        body.addWidget(group)

        bottom = QHBoxLayout()
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(True)

        self.generate_btn = QPushButton("Generate Report")
        self.generate_btn.setMinimumHeight(42)
        self.generate_btn.clicked.connect(self.generate_report)

        bottom.addWidget(self.progress, 1)
        bottom.addWidget(self.generate_btn)

        body.addLayout(bottom)

        self.status = QLabel("Status: Ready")
        body.addWidget(self.status)

        main.addLayout(body)
        self.setCentralWidget(root)

    def _path_row(self, label_text, line_edit, callback):
        layout = QVBoxLayout()
        label = QLabel(label_text)
        row = QHBoxLayout()

        btn = QPushButton("Browse")
        btn.clicked.connect(callback)

        row.addWidget(line_edit, 1)
        row.addWidget(btn)

        layout.addWidget(label)
        layout.addLayout(row)
        return layout

    def browse_input(self):
        path = QFileDialog.getExistingDirectory(self, "Select AutoSupport Folder")
        if path:
            self.input_path.setText(path)

    def browse_output(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Select Output Excel",
            self.output_path.text(),
            "Excel Files (*.xlsx)",
        )
        if path:
            self.output_path.setText(path)

    def generate_report(self):
        input_path = self.input_path.text().strip()

        if not input_path:
            QMessageBox.warning(
                self,
                "Missing Input",
                "Please select AutoSupport folder / ZIP / file.",
            )
            return

        self.progress.setValue(10)
        self.status.setText("Status: Scanning AutoSupport files...")

        try:
            parser = AutoSupportParser(input_path)
            records = parser.parse_capacity_records()
            files = parser.find_files()

            self.progress.setValue(60)
            self.status.setText(f"Status: Found {len(files)} candidate files.")

            if not files:
                QMessageBox.warning(
                    self,
                    "No Files Found",
                    "No supported AutoSupport files were found.\n\nSupported: .xml, .txt, .log, .json",
                )
                self.progress.setValue(0)
                self.status.setText("Status: No files found.")
                return

            print("Found AutoSupport candidate files:")
            for f in files[:20]:
                print(f)

            if len(files) > 20:
                print(f"... and {len(files) - 20} more files")

            self.progress.setValue(100)
            self.status.setText(f"Status: Scan completed. Found {len(files)} files.")

            print("Parsed capacity records:")
            for r in records:
                print(r)

            self.progress.setValue(100)
            self.status.setText(
                f"Status: Scan completed. Found {len(files)} files. Parsed {len(records)} records."
            )

            QMessageBox.information(
                self,
                "Scan Completed",
                f"Found {len(files)} candidate files.\nParsed {len(records)} capacity records.",
            )

        except Exception as e:
            self.progress.setValue(0)
            self.status.setText("Status: Error")
            QMessageBox.critical(self, "Error", str(e))