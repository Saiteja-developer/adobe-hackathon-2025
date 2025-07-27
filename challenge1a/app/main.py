import os
import json
import fitz  # PyMuPDF
from utils import extract_outline

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def main():
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            try:
                input_path = os.path.join(INPUT_DIR, filename)
                doc = fitz.open(input_path)
                title, outline = extract_outline(doc)
                output_data = {
                    "title": title,
                    "outline": outline
                }

                output_filename = filename.replace(".pdf", ".json")
                output_path = os.path.join(OUTPUT_DIR, output_filename)
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(output_data, f, indent=2, ensure_ascii=False)

                print(f"Processed: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    main()
