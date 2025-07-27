from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def keyword_boost_score(score, block, doc_name, persona, job):
    text = block["text"].lower()
    doc = doc_name.lower()
    combined = f"{text} {doc} {persona.lower()} {job.lower()}"
    boost = 1.0

    topic_boosts = {
        # Universal academic/research terms
        "methodology": 1.3, "dataset": 1.3, "benchmark": 1.2,
        "analysis": 1.2, "results": 1.2, "findings": 1.3,
        "conclusion": 1.1, "summary": 1.2,

        # Business/financial
        "revenue": 1.3, "profit": 1.2, "r&d": 1.3, "strategy": 1.2, "investment": 1.3,

        # Education
        "reaction": 1.3, "mechanism": 1.2, "concept": 1.2, "example": 1.2,

        # HR / compliance
        "form": 1.3, "fillable": 1.4, "signature": 1.2, "workflow": 1.2,

        # Travel
        "itinerary": 1.3, "destination": 1.3, "places": 1.2,

        # Food
        "vegetarian": 1.3, "dish": 1.2, "recipe": 1.2, "gluten-free": 1.3,

        # Science / engineering
        "architecture": 1.2, "design": 1.2, "model": 1.2, "system": 1.1
    }

    penalizers = ["copyright", "footer", "index", "advertisement", "contact us"]

    for k, val in topic_boosts.items():
        if k in combined:
            boost *= val

    if any(p in text for p in penalizers):
        boost *= 0.4  # Strongly penalize irrelevant metadata

    return score * boost

def rank_blocks(query, doc_blocks, persona, job):
    all_blocks = []
    sources = []

    for doc in doc_blocks:
        for block in doc["blocks"]:
            all_blocks.append(block["text"])
            sources.append({
                "document": doc["document"],
                "page": block["page"],
                "text": block["text"]
            })

    if not all_blocks:
        return []

    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([query] + all_blocks)
    query_vec = vectors[0]
    block_vecs = vectors[1:]

    scores = cosine_similarity(query_vec, block_vecs).flatten()
    ranked = []
    for i, score in enumerate(scores):
        boosted = keyword_boost_score(score, sources[i], sources[i]["document"], persona, job)
        ranked.append({**sources[i], "score": float(boosted)})

    # One section per document (score-wise)
    final = []
    seen_docs = set()
    for block in sorted(ranked, key=lambda x: -x["score"]):
        if block["document"] not in seen_docs:
            final.append(block)
            seen_docs.add(block["document"])
        if len(final) == 5:
            break

    return final
