import re
from models import Submission, AuthorOutput, ReviewOutput


# ----------------------------
# Section Parsing
# ----------------------------

def split_sections(text: str):
    sections = {
        "abstract": "",
        "methods": "",
        "results": "",
        "conclusion": ""
    }

    lower_text = text.lower()

    def extract_section(start_keyword, end_keywords):
        start = lower_text.find(start_keyword)
        if start == -1:
            return ""
        end = len(text)
        for keyword in end_keywords:
            pos = lower_text.find(keyword, start + 1)
            if pos != -1:
                end = min(end, pos)
        return text[start:end]

    sections["abstract"] = extract_section("abstract", ["introduction", "methods", "results"])
    sections["methods"] = extract_section("methods", ["results", "conclusion"])
    sections["results"] = extract_section("results", ["conclusion"])
    sections["conclusion"] = extract_section("conclusion", [])

    return sections


# ----------------------------
# Claim Extraction
# ----------------------------

STRONG_LANGUAGE = [
    "guarantee",
    "100%",
    "perfect",
    "always",
    "never",
    "cure",
    "eliminate",
    "all cases"
]

MODERATE_LANGUAGE = [
    "demonstrate",
    "achieved",
    "improve",
    "suggest",
    "indicate"
]


def extract_claims(text: str):
    sentences = re.split(r'[.?!]', text)
    claims = []

    for sentence in sentences:
        sentence_lower = sentence.lower()

        if any(word in sentence_lower for word in STRONG_LANGUAGE + MODERATE_LANGUAGE):
            claims.append(sentence.strip())

    return " ".join(claims) if claims else text[:300]


# ----------------------------
# Confidence Inference
# ----------------------------

def infer_confidence(claims: str):
    claims_lower = claims.lower()

    if any(word in claims_lower for word in STRONG_LANGUAGE):
        return 0.95
    elif any(word in claims_lower for word in MODERATE_LANGUAGE):
        return 0.75
    return 0.6


# ----------------------------
# Dataset Detection
# ----------------------------

def detect_dataset(text: str):
    dataset_keywords = ["dataset", "publicly available", "samples", "participants"]
    return any(word in text.lower() for word in dataset_keywords)


# ----------------------------
# Author Agent
# ----------------------------

def author_agent(submission: Submission) -> AuthorOutput:
    text = submission.paper_text

    sections = split_sections(text)

    results_section = sections["results"] if sections["results"] else text

    claims = extract_claims(results_section)
    confidence = infer_confidence(claims)

    return AuthorOutput(
        structured_claims=claims,
        confidence_score=confidence
    )


# ----------------------------
# Reviewer Agent
# ----------------------------

def reviewer_agent(submission: Submission) -> ReviewOutput:
    text = submission.paper_text

    novelty_score = 0.8
    methodology_score = 0.7
    ethical_flags = []

    if "human trial" in text.lower() and "consent" not in text.lower():
        ethical_flags.append("Missing consent for human trial")

    if not detect_dataset(text):
        ethical_flags.append("No dataset mentioned")

    return ReviewOutput(
        novelty_score=novelty_score,
        methodology_score=methodology_score,
        ethical_flags=ethical_flags
    )