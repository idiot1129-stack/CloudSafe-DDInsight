from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font


class ExcelReport:

    def create_summary(self, records, output_file):

        wb = Workbook()

        ws = wb.active
        ws.title = "Summary"

        headers = [
            "Generated Time",
            "Hostname",
            "Model",
            "Serial",
            "DDOS",
            "Pre-Comp Used (TiB)",
            "Post-Comp Used (TiB)",
            "Post-Comp Size (TiB)",
            "Available (TiB)",
            "Usage %",
        ]

        for col, header in enumerate(headers, start=1):
            cell = ws.cell(row=1, column=col)
            cell.value = header
            cell.font = Font(bold=True)

        row = 2

        for r in records:

            ws.cell(row=row, column=1).value = r["generated_time"]
            ws.cell(row=row, column=2).value = r["hostname"]
            ws.cell(row=row, column=3).value = r["model"]
            ws.cell(row=row, column=4).value = r["serial"]
            ws.cell(row=row, column=5).value = r["ddos"]
            ws.cell(row=row, column=6).value = r["pre_comp_used_tib"]
            ws.cell(row=row, column=7).value = r["post_comp_used_tib"]
            ws.cell(row=row, column=8).value = r["post_comp_size_tib"]
            ws.cell(row=row, column=9).value = r["post_comp_avail_tib"]
            ws.cell(row=row, column=10).value = r["use_pct"]

            row += 1

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        wb.save(output_file)