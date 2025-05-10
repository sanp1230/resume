import re
from collections import Counter

def extract_keywords(text, top_n=15):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    stop_words = {"with", "from", "that", "this", "have", "will", "your", "they", "been", "into", "more", "some"}
    words = [w for w in words if w not in stop_words]
    most_common = Counter(words).most_common(top_n)
    return [word for word, count in most_common]

def rule_based_score(resume_text, job_description):
    jd_keywords = extract_keywords(job_description)
    resume_words = resume_text.lower()

    matched = [kw for kw in jd_keywords if kw in resume_words]
    match_percent = len(matched) / len(jd_keywords) * 100

    return {
        "rule_score": round(match_percent),
        "jd_keywords": jd_keywords,
        "matched_keywords": matched,
        "missing_keywords": list(set(jd_keywords) - set(matched))
    } 