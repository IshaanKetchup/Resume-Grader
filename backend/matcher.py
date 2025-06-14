from sentence_transformers import SentenceTransformer, util
import re
import numpy as np

# Load E5 model (trained to understand "query: ..." and "passage: ...")
model = SentenceTransformer("intfloat/e5-small-v2")

# --- Smart section splitter ---
def split_into_sections(resume_text: str) -> dict:
    lines = resume_text.splitlines()
    sections = {}
    current_section = "Other"

    for line in lines:
        if re.match(r'^([A-Z][A-Za-z ]{2,30})$', line.strip()) and len(line.strip().split()) <= 4:
            current_section = line.strip()
            sections[current_section] = ""
        else:
            sections.setdefault(current_section, "")
            sections[current_section] += " " + line.strip()

    return sections

# --- Main similarity function ---
def compute_similarity(job_desc: str, resume_text: str, weighted: bool = False) -> dict:
    # Encode JD with proper prefix for E5
    job_emb = model.encode(f"query: {job_desc}", normalize_embeddings=True)

    sections = split_into_sections(resume_text)
    scores = {}
    weights = {}

    for section, text in sections.items():
        if not text.strip():
            continue
        # Encode section with passage prefix
        res_emb = model.encode(f"passage: {text}", normalize_embeddings=True)
        # Compute cosine similarity
        score = util.cos_sim(job_emb, res_emb)[0][0].item() * 100
        scores[section] = round(score, 2)
        weights[section] = len(text.split())

    # Compute final score
    if not scores:
        return {"section_scores": {}, "match_percent": 0.0}

    if weighted:
        total_weight = sum(weights.values())
        weighted_avg = sum(scores[sec] * weights[sec] for sec in scores) / total_weight
        final_score = round(weighted_avg, 2)
    else:
        final_score = round(np.mean(list(scores.values())), 2)

    return {
        "section_scores": scores,
        "match_percent": final_score
    }
