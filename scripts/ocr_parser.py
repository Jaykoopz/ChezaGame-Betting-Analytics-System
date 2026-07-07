from pathlib import Path
import pytesseract
from PIL import Image


class OCRParser:
    def __init__(self):
        # Change this path if Tesseract is installed elsewhere
        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

        self.image_folder = Path("data/screenshots")
        self.output_folder = Path("data/processed")

        self.output_folder.mkdir(parents=True, exist_ok=True)

    def process_images(self):

        images = []

        images.extend(self.image_folder.glob("*.png"))
        images.extend(self.image_folder.glob("*.jpg"))
        images.extend(self.image_folder.glob("*.jpeg"))

        print("=" * 60)
        print("CBAS OCR ENGINE")
        print("=" * 60)

        print(f"Images Found : {len(images)}\n")

        for image in sorted(images):

            print(f"Reading {image.name}")

            text = pytesseract.image_to_string(Image.open(image))

            output_file = self.output_folder / f"{image.stem}.txt"

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)

            print("✓ OCR Complete")

        print("\nAll screenshots processed successfully.")