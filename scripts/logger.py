from pathlib import Path


class ParserLogger:

    def __init__(self):
        self.folder = Path("logs")
        self.folder.mkdir(exist_ok=True)

        self.file = self.folder / "parser_errors.txt"

        # Clear previous log
        self.file.write_text("", encoding="utf-8")

    def log(self, filename, message, text):

        with open(self.file, "a", encoding="utf-8") as f:

            f.write("=" * 70 + "\n")
            f.write(f"FILE: {filename}\n")
            f.write(f"ERROR: {message}\n\n")
            f.write(text)
            f.write("\n\n")