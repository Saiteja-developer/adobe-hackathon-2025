import os
import json
from datetime import datetime

from src.parse_pdf import extract_text_by_page
from src.semantic_ranker import rank_blocks
from src.summarizer import refine_text
from src.generate_output import generate_output

def run(input_path, pdf_dir, output_path):
    # Step 1: Load input JSON
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error loading input JSON: {e}")
        return

    # Step 2: Extract persona + job
    persona = config.get("persona", {}).get("role", "Generic User")
    job = config.get("job_to_be_done", {}).get("task", "")
    query = f"{persona} {job}"
    documents = config.get("documents", [])

    if not documents:
        print("No documents specified in input JSON.")
        return

    # Step 3: Extract text blocks from all input PDFs
    docs = []
    for doc in documents:
        path = os.path.join(pdf_dir, doc["filename"])
        try:
            blocks = extract_text_by_page(path)
            docs.append({
                "document": doc["filename"],
                "blocks": blocks
            })
        except Exception as e:
            print(f"Error processing {doc['filename']}: {e}")

    if not docs:
        print("No valid documents parsed. Exiting.")
        return

    # Step 4: Rank blocks using semantic relevance
    ranked = rank_blocks(query, docs, persona=persona, job=job)

    # Debug: Print top 5 scores
    print("\nTop 5 Ranked Blocks (debug):")
    for i, blk in enumerate(sorted(ranked, key=lambda x: -x["score"])[:5]):
        print(f"[Score {i+1}] {blk['score']:.4f} from {blk['document']} page {blk['page']}")

    # Step 5: Refine subsection content
    for block in ranked:
        block["refined"] = refine_text(block["text"])

    # Step 6: Prepare metadata
    metadata = {
        "input_documents": [doc["filename"] for doc in documents],
        "persona": persona,
        "job_to_be_done": job
    }

    # Step 7: Generate final output JSON
    generate_output(metadata, ranked, output_path)
    print("Output written successfully for", os.path.basename(output_path))


def run_collection(collection_id):
    input_path = f"{collection_id}/challenge1b_input.json"
    pdf_dir = f"{collection_id}/PDFs"
    output_path = f"{collection_id}/challenge1b_output.json"
    run(input_path, pdf_dir, output_path)


if __name__ == "__main__":
    for cid in ["Collection_1", "Collection_2", "Collection_3"]:
        print(f"\nProcessing {cid} ...")
        run_collection(cid)
