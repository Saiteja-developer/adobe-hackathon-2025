from collections import defaultdict
import unicodedata
import numpy as np
from sklearn.cluster import KMeans

def extract_outline(doc):
    font_scores = defaultdict(int)
    heading_candidates = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict").get("blocks", [])

        for b in blocks:
            for line in b.get("lines", []):
                spans = line.get("spans", [])
                if not spans or not isinstance(spans, list):
                    continue

                valid_spans = [s for s in spans if "text" in s and "size" in s and s["text"].strip()]
                if not valid_spans:
                    continue

                text = " ".join(span["text"].strip() for span in valid_spans)
                text = unicodedata.normalize("NFC", text)

                if len(text) < 5 or not any(char.isalnum() for char in text):
                    continue

                font_size = valid_spans[0].get("size", 0)
                font = valid_spans[0].get("font", "")
                is_bold = "bold" in font.lower()

                heading_candidates.append({
                    "text": text,
                    "size": font_size,
                    "bold": is_bold,
                    "page": page_num
                })

                font_scores[font_size] += 1

    if not heading_candidates:
        return "Untitled Document", []

    sizes = np.array(list(font_scores.keys())).reshape(-1, 1)
    try:
        kmeans = KMeans(n_clusters=min(3, len(sizes)), n_init="auto", random_state=0).fit(sizes)
    except Exception:
        return "Untitled Document", []

    sorted_centers = sorted([(c[0], i) for i, c in enumerate(kmeans.cluster_centers_)], reverse=True)
    level_map = {sorted_centers[i][1]: level for i, level in enumerate(["H1", "H2", "H3"])}
    font_to_level = {size[0]: level_map[cluster] for size, cluster in zip(sizes, kmeans.labels_)}

    seen = set()
    outline = []
    for h in heading_candidates:
        if h["size"] not in font_to_level:
            continue
        text = h["text"].strip()
        if text.lower() in seen:
            continue
        seen.add(text.lower())
        if not h["bold"] and h["size"] < 10:
            continue
        outline.append({
            "level": font_to_level[h["size"]],
            "text": text,
            "page": h["page"]
        })

    title = doc.metadata.get("title", "")
    if not title and outline:
        title = outline[0]["text"]
    if not title:
        title = "Untitled Document"

    return title, outline
