# Challenge 1a: PDF Outline Extraction Engine

## Overview
This repository contains our solution for Challenge 1a of the Adobe India Hackathon 2025.  
The objective is to extract structured outlines (Title, H1, H2, H3 headings with page numbers) from input PDF files.

---

## Official Challenge Requirements

- **GitHub Repository:** Private, with complete source code
- **Dockerfile:** Must be present and support `linux/amd64`
- **README.md:** Must describe architecture, libraries used, and execution process

---

## Quick Start

### Build the Docker Image

```sh
docker build --platform linux/amd64 -t pdf-outline-extractor:final .
```

### Run the Docker Container

#### On Linux/macOS
```sh
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-outline-extractor:final
```

#### On Windows PowerShell
```ps1
docker run --rm `
  -v ${PWD}\input:/app/input:ro `
  -v ${PWD}\output:/app/output `
  --network none `
  pdf-outline-extractor:final
```

---

## Constraints

- **Execution Time:** ≤ 10 seconds (for 50 pages)
- **Model Size:** ≤ 200MB
- **Network:** Offline only
- **Platform:** CPU-only, AMD64 architecture
- **Input Folder:** Mounted as read-only

---

## Solution Structure

```
challenge_1a/
├── app/
│   ├── main.py            # Entry point for batch PDF processing
│   ├── utils.py           # Heading detection and classification logic
│   └── requirements.txt   # Python dependencies
├── input/                 # Input PDF files (mounted)
├── output/                # Output JSONs
├── Dockerfile             # Docker image builder
├── .dockerignore          # Ignore unnecessary files
└── README.md              # Documentation (this file)
```

---

## Highlights

- **Extracts Title, H1, H2, H3** using:
  - KMeans font size clustering
  - Positional & styling heuristics
  - Unicode normalization for multilingual inputs
- **Handles multi-column layouts**
- **Supports** Japanese, French, and Spanish
- **Uses PyMuPDF** for fast layout parsing

---

## Output Format (example)

```json
{
  "title": "Parsippany -Troy Hills STEM Pathways",
  "outline": [
    {
      "level": "H1",
      "text": "Parsippany -Troy Hills STEM Pathways",
      "page": 1
    }
  ]
}
```

- Each PDF in `/app/input/` produces a `.json` in `/app/output/` with:
  - `"title"`: Inferred document title
  - `"outline"`: List of heading objects (level, text, page)

---

## Dockerfile Reference

```dockerfile
FROM --platform=linux/amd64 python:3.10-slim
WORKDIR /app
COPY app/ /app/
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

---

## Implementation Guidelines

- **Performance**
  - Filters text spans (removes empty lines, footnotes)
  - Uses font-based clustering for heading detection
  - Unicode support via `unicodedata`
- **Robustness**
  - Handles PDFs with/without titles
  - Detects heading hierarchies, even with inconsistent fonts
  - No hardcoding; works with unseen, noisy PDFs

---

## Testing Locally

### Linux/macOS

```sh
docker build --platform linux/amd64 -t pdf-outline-extractor:final .
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-outline-extractor:final
```

### Windows PowerShell

```ps1
docker build --platform linux/amd64 -t pdf-outline-extractor:final .
docker run --rm `
  -v ${PWD}\input:/app/input:ro `
  -v ${PWD}\output:/app/output `
  --network none `
  pdf-outline-extractor:final
```

---

## Validation Checklist

- [ ] All PDFs processed from `/app/input/`
- [ ] Outputs written as `/app/output/filename.json`
- [ ] Output structure matches schema
- [ ] ≤ 10 seconds processing for 50-page PDF
- [ ] No internet dependency during execution
- [ ] ≤ 16GB memory usage
- [ ] Fully offline and CPU-compliant
