import json
import re
from datetime import datetime
import os

def generate_output(metadata, ranked_sections, out_path="challenge1b_output.json"):
    extracted = []
    subsection_analysis = []

    for i, item in enumerate(ranked_sections):
        lines = item["text"].split("\n")

        # Prefer first informative-looking line (non-bullet, >5 words, proper case)
        raw_title = next(
            (line for line in lines if len(line.split()) > 5 and not line.lower().startswith("o ")),
            lines[0]
        )

        # Clean noisy characters
        section_title = re.sub(r"[^a-zA-Z0-9: ,.'\"()-]", "", raw_title).strip()[:100]

        if not section_title or len(section_title.split()) < 2:
            section_title = f"Relevant Section from Page {item['page']}"

        refined = item.get("refined", "").strip()

        extracted.append({
            "document": item["document"],
            "section_title": section_title,
            "importance_rank": i + 1,
            "page_number": item["page"]
        })

        subsection_analysis.append({
            "document": item["document"],
            "refined_text": refined if refined else item["text"],
            "page_number": item["page"]
        })

    result = {
        "metadata": {
            "input_documents": metadata["input_documents"],
            "persona": metadata["persona"],
            "job_to_be_done": metadata["job_to_be_done"],
            "timestamp": datetime.now().isoformat()
        },
        "extracted_sections": extracted,
        "subsection_analysis": subsection_analysis
    }

    try:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Output saved to: {out_path}")
    except Exception as e:
        print(f"Failed to save output JSON: {e}")

    log_path = os.path.join(os.path.dirname(out_path), "log.txt")
    with open(log_path, "w", encoding="utf-8") as logf:
        for sec in extracted:
            logf.write(f"[{sec['importance_rank']}] {sec['document']} - {sec['section_title']} (page {sec['page_number']})\n")
