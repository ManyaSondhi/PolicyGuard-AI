from models import AuthorOutput, ReviewOutput, PolicyResult

ABSOLUTE_TERMS = ["100%", "guarantee", "always", "never", "cure", "perfect"]


def evaluate_policy(author: AuthorOutput, review: ReviewOutput):

    violations = []
    modified_claims = author.structured_claims
    risk_score = 0

    # ------------------------------------
    # Rule 1: Absolute Claims (High)
    # ------------------------------------
    for term in ABSOLUTE_TERMS:
        if term.lower() in modified_claims.lower():
            violations.append(f"Absolute claim detected: '{term}'")
            risk_score += 3

    # ------------------------------------
    # Rule 2: Overconfidence (Medium)
    # ------------------------------------
    if author.confidence_score > 0.85:
        violations.append("Overconfidence detected")
        risk_score += 2

    # ------------------------------------
    # Rule 3: Ethical Flags (Critical)
    # ------------------------------------
    if review.ethical_flags:
        for flag in review.ethical_flags:
            violations.append(flag)
            risk_score += 5

    # ------------------------------------
    # Rule 4: Dataset Evidence Required
    # ------------------------------------
    if "dataset" not in modified_claims.lower():
        violations.append("No dataset evidence provided")
        risk_score += 2

    # ------------------------------------
    # Soft Rewrite Layer
    # ------------------------------------
    if violations:
        modified_claims = modified_claims.replace("guarantees", "suggests")
        modified_claims = modified_claims.replace("guarantee", "suggests")
        modified_claims = modified_claims.replace("100%", "high")
        modified_claims = modified_claims.replace("cures", "may help treat")
        modified_claims = modified_claims.replace("cure", "may help treat")

    approved = risk_score == 0

    # ------------------------------------
    # Governance Summary
    # ------------------------------------
    governance_summary = f"""
Governance Risk Assessment:
Total Violations: {len(violations)}
Computed Risk Score: {risk_score}

Decision Basis:
- Absolute claims increase scientific misrepresentation risk.
- Overconfidence indicates exaggerated certainty.
- Missing dataset evidence reduces reproducibility.
"""

    # ------------------------------------
    # Reasoning Trace (AI thinking)
    # ------------------------------------
    reasoning_trace = [
        "Section-aware parsing completed",
        "Claims extracted from Results section",
        f"Inferred confidence score: {author.confidence_score}",
        f"Dataset detected: {'Yes' if 'dataset' in author.structured_claims.lower() else 'No'}",
        f"Total violations identified: {len(violations)}",
        f"Computed risk score: {risk_score}"
    ]

    # ------------------------------------
    # Delegation Trace (Multi-agent flow)
    # ------------------------------------
    delegation_trace = [
        "Author Agent structured scientific claims",
        "Reviewer Agent evaluated novelty and methodology",
        "Policy Engine applied deterministic governance rules",
        "Risk score computed and validated against policy"
    ]

    return PolicyResult(
        approved=approved,
        violations=violations,
        risk_score=risk_score,
        modified_claims=modified_claims,
        governance_summary=governance_summary,
        reasoning_trace=reasoning_trace,
        delegation_trace=delegation_trace
    )