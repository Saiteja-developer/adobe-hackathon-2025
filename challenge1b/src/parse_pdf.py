import pdfplumber

def extract_text_by_page(pdf_path):
    blocks = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if not text:
                    continue

                lines = text.split("\n")
                cleaned = []
                for line in lines:
                    line = line.strip()
                    if len(line) < 15:
                        continue
                    if any(line.lower().startswith(x) for x in ["page", "copyright", "printed", "all rights reserved"]):
                        continue
                    cleaned.append(line)

                joined = "\n".join(cleaned).strip()
                if len(joined) > 40:
                    blocks.append({
                        "page": page_num,
                        "text": joined
                    })
    except Exception as e:
        print(f"Failed to parse {pdf_path}: {e}")
    return blocks
