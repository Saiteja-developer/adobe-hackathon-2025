
# Challenge 1b: Persona-Driven Document Intelligence

## Overview

This repository contains our solution for **Challenge 1b** of the Adobe India Hackathon 2025.  
**Objective:** Analyze a collection of related PDFs based on a specific persona and job-to-be-done.  
**Key Features:**

- **Offline-first**
- **CPU-only**
- **Domain-agnostic**
- Supports multiple persona-task combinations across diverse sectors (travel, education, business, food, etc.)

---

## Official Challenge Guidelines

**Submission Requirements:**

- **GitHub Repository:** Private, with all code and sample outputs
- **Dockerfile:** Must target `linux/amd64`
- **README.md:** Must document architecture, libraries used, and execution instructions

**Constraints:**

- **Execution Time:** ≤ 60 seconds
- **Model Size:** ≤ 1 GB
- **Network:** Offline only
- **Platform:** CPU-only

**Output:** Structured JSON with:
- `metadata`
- `extracted_sections`
- `subsection_analysis`

---

## Build & Run Instructions

**Build Image:**
```sh
docker build --platform linux/amd64 -t adobe-1b-runner .
```

**Run (Linux/macOS):**
```sh
docker run --rm \
  -v $(pwd):/app \
  --network none \
  adobe-1b-runner
```

**Run (Windows PowerShell):**
```powershell
docker run --rm `
  -v ${PWD}:/app `
  --network none `
  adobe-1b-runner
```

---

## Solution Structure

```
Challenge_1b/
├── Collection_1/
│   ├── PDFs/
│   ├── challenge1b_input.json
│   └── challenge1b_output.json
├── Collection_2/
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
```

---

## Libraries Used

- **pdfplumber**: PDF parsing and layout extraction  
- **scikit-learn**: TF-IDF vectorization and cosine similarity  
- **numpy**: Vector operations and matrix transformations  
- **nltk**: Sentence tokenization and extractive summarization  

---

## Performance Strategy

- Extracts block-level text from all pages
- Filters low-density or noisy blocks
- Scores relevance using TF-IDF + cosine similarity
- Summarizes top 5 blocks using sentence ranking
- Fully domain- and language-agnostic (no hardcoding)

---

## Output Format: `challenge1b_output.json`

```json
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
```

---

## Validation Checklist

- [x] All collections processed in sequence (Collection_1, Collection_2, ...)
- [x] Each collection contains `PDFs/` and `challenge1b_input.json`
- [x] Output written as `challenge1b_output.json` in the same folder
- [x] Fully offline execution (no internet access)
- [x] End-to-end runtime ≤ 60 seconds on CPU
- [x] Output format and structure match the specification

---
