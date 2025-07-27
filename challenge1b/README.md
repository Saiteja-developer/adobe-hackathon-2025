Challenge 1b: Persona-Driven Document Intelligence

Overview
--------------
This repository contains our solution for Challenge 1b of the Adobe India Hackathon 2025. The objective is to analyze a collection of related PDFs based on a specific persona and job-to-be-done. The goal is to extract the five most relevant sections from the documents and summarize them with their refined content in a structured JSON output.

The system is:
Offline-first
CPU-only
Domain-agnostic
Supports multiple persona-task combinations across diverse sectors like travel, education, business, and food

Official Challenge Guidelines
Submission Requirements
-------------------------
GitHub Repository: Private with all code and sample outputs
Dockerfile: Must target linux/amd64
README.md: Should document architecture, libraries used, and execution instructions

Constraints
------------------------
Execution Time: ≤ 60 seconds
Model Size: ≤ 1 GB
Network: Offline only
Platform: CPU-only
Output: Structured JSON with:
metadata
extracted_sections
subsection_analysis

Build Command
--------------
bash
docker build --platform linux/amd64 -t adobe-1b-runner .

Run Command (Linux/macOS)
bash
docker run --rm \
  -v $(pwd):/app \
  --network none \
  adobe-1b-runner

Run Command (Windows PowerShell)

docker run --rm `
  -v ${PWD}:/app `
  --network none `
  adobe-1b-runner


Solution Structure
----------------------
Challenge_1b/
├── Collection_1/
│   ├── PDFs/
│   ├── challenge1b_input.json
│   └── challenge1b_output.json
├── Collection_2/                  # You can add any number of collections
│   ├── PDFs/
│   ├── challenge1b_input.json
│   └── challenge1b_output.json
├── src/
│   ├── main.py
│   ├── parse_pdf.py
│   ├── semantic_ranker.py
│   ├── summarizer.py
│   └── generate_output.py
├── Dockerfile
├── requirements.txt
├── README.md
└── approach_explanation.md

Libraries Used
------------------
pdfplumber: PDF parsing and layout extraction
scikit-learn: TF-IDF vectorization and cosine similarity
numpy: Vector operations and matrix transformations
nltk: Sentence tokenization and extractive summarization

Performance Strategy
---------------------------
Extracts block-level text from all pages
Filters low-density or noisy blocks
Scores relevance using TF-IDF + cosine similarity
Summarizes top 5 blocks using sentence ranking
Works without hardcoding domain or language

Output Format (challenge1b_output.json)
---------------------------------------
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "HR professional",
    "job_to_be_done": "Create and manage fillable forms",
    "timestamp": "2025-07-25T10:00:00"
  },
  "extracted_sections": [
    {
      "document": "doc2.pdf",
      "section_title": "Creating Forms in Acrobat",
      "importance_rank": 1,
      "page_number": 3
    }
  ],
  "subsection_analysis": [
    {
      "document": "doc2.pdf",
      "refined_text": "To create a fillable form, use the 'Prepare Form' tool...",
      "page_number": 3
    }
  ]
}


Validation Checklist
-------------------------------
All collections processed in sequence (Collection_1, Collection_2, ...)
Each collection contains PDFs/ and challenge1b_input.json
Output written as challenge1b_output.json in the same folder
Fully offline execution (no internet access)
End-to-end runtime ≤ 60 seconds on CPU
Output format and structure match the specification