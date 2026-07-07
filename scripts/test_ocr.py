import pytesseract
from PIL import Image
from pathlib import Path

# Set the Tesseract executable location
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Folder containing screenshots
image_folder = Path("data/screenshots")

# Find all PNG, JPG and JPEG images
images = (
    list(image_folder.glob("*.png")) +
    list(image_folder.glob("*.jpg")) +
    list(image_folder.glob("*.jpeg"))
)

print("=" * 60)
print("CBAS OCR TEST")
print("=" * 60)

print(f"Images found: {len(images)}")

if len(images) == 0:
    print("❌ No screenshots found.")
    exit()

image = images[0]

print(f"\nReading image:")
print(image.name)

text = pytesseract.image_to_string(Image.open(image))

print("\n" + "=" * 60)
print("OCR RESULT")
print("=" * 60)

print(text[:5000])