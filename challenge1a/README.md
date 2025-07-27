Challenge 1a: PDF Outline Extraction Engine

Overview
This repository contains our solution for Challenge 1a of the Adobe India Hackathon 2025. The objective is to extract structured outlines (Title, H1, H2, H3 headings with page numbers) from input PDF files and export them as clean, standardized JSONs. The solution is optimized for speed, accuracy, multilingual support, and offline usage inside a Docker container running on AMD64 CPUs.

Official Challenge Guidelines

Submission Requirements
- GitHub Repository: Private project with complete source code
- Dockerfile: Must be present and support linux/amd64
- README.md: Describes architecture, libraries used, and execution process

Build Command
docker build --platform linux/amd64 -t pdf-outline-extractor:final .

Run Command (Linux/macOS)
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-outline-extractor:final

Run Command (Windows PowerShell)
docker run --rm `
  -v ${PWD}\input:/app/input:ro `
  -v ${PWD}\output:/app/output `
  --network none `
  pdf-outline-extractor:final

Constraints
Execution Time: ≤ 10 seconds (50 pages)
Model Size: ≤ 200MB
Network: Offline only
Runtime Platform: CPU-only, AMD64 arch
Input Folder: Mounted read-only

Solution Structure
Challenge_1a/
├── app/
│   ├── main.py              # Entry point for batch PDF processing
│   ├── utils.py             # Heading detection and classification logic
│   └── requirements.txt     # Python dependencies
├── input/                   # Directory for input PDF files (mounted)
├── output/                  # Directory where output JSONs are saved
├── Dockerfile               # Builds the Docker image
├── .dockerignore            # Ignore unnecessary files
└── README.md                # This documentation file

Sample Implementation

Highlights
- Extracts Title, and detects H1, H2, H3 levels using:
  - Font size clustering via KMeans
  - Positional and styling heuristics
  - Unicode normalization for multilingual inputs
- Works on multi-column layouts
- Fully compatible with Japanese, French, and Spanish
- Uses PyMuPDF for fast layout parsing

Output Sample
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

Docker Configuration
FROM --platform=linux/amd64 python:3.10-slim
WORKDIR /app
COPY app/ /app/
RUN pip install -r requirements.txt
CMD ["python", "main.py"]

Expected Output Format
Each PDF file in the /app/input/ directory will generate a corresponding .json file in /app/output/ following this structure:

- "title": Inferred document title
- "outline": Array of heading objects
  - "level": H1 / H2 / H3
  - "text": Heading content
  - "page": Page number (1-indexed)

Implementation Guidelines

Performance Strategy
- Text span filtering to exclude empty lines or footnotes
- Font-based clustering for accurate heading level detection
- Multilingual Unicode support via unicodedata

Robustness
- Handles PDFs without a Title
- Detects heading hierarchies even with inconsistent fonts
- No hardcoding; works on unseen, noisy PDFs

Testing Your Solution
------------------------
Local Testing (Linux/macOS)
docker build --platform linux/amd64 -t pdf-outline-extractor:final .
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-outline-extractor:final

Local Testing (PowerShell)
docker build --platform linux/amd64 -t pdf-outline-extractor:final .
docker run --rm `
  -v ${PWD}\input:/app/input:ro `
  -v ${PWD}\output:/app/output `
  --network none `
  pdf-outline-extractor:final

Validation Checklist
-----------------------
- All PDFs processed from /app/input/
- Outputs written as /app/output/filename.json
- Output structure matches required schema
- ≤ 10 seconds processing time for 50-page PDF
- No internet dependency during execution
- Memory usage ≤ 16GB
- Fully offline and CPU-compliant
