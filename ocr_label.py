import cv2
import easyocr
import os

# Initialize OCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Folder where YOLO prediction images are saved
image_folder = "runs/detect/predict2"

# Keywords we care about
important_keywords = [
    "MODEL", "DC", "V", "LED", "ROLL", "QTY", "STRIP", "WATT", "CATEGORY"
]

print("\n🔍 Starting OCR on detected images\n")
print("-" * 40)

for file in os.listdir(image_folder):
    if file.lower().endswith((".jpg", ".jpeg", ".png")):
        img_path = os.path.join(image_folder, file)
        print(f"\n📄 Processing: {file}")

        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        results = reader.readtext(gray)

        if len(results) == 0:
            print("  ❌ No text detected")
            continue

        for (bbox, text, conf) in results:
            clean_text = text.upper().strip()

            if conf > 0.4:
                for key in important_keywords:
                    if key in clean_text:
                        print(f"  ✅ {clean_text} (conf={conf:.2f})")

print("\n✔ OCR completed")




import csv

po_model = "BNZ-2835-48"
po_qty = "70"

print("\n🔎 Verifying against PO...\n")

detected_model = False
detected_qty = False

for (bbox, text, conf) in results:
    t = text.upper()

    if po_model in t:
        detected_model = True

    if po_qty in t:
        detected_qty = True

if detected_model and detected_qty:
    print("✅ GRN MATCHED — Goods Accepted")
else:
    print("❌ GRN MISMATCH — Manual Check Required")
