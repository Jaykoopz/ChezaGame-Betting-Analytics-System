from pathlib import Path
from datetime import datetime


class ReportGenerator:

    def __init__(self):
        self.folder = Path("reports")
        self.folder.mkdir(exist_ok=True)

    def save(self, text):

        filename = self.folder / (
            f"CBAS_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        with open(filename, "w", encoding="utf-8") as file:
            file.write(text)

        print(f"\nReport saved successfully:")
        print(filename)