from pydantic import BaseModel
from typing import List, Optional


# =========================
# USER POLICY
# =========================

class UserPolicy(BaseModel):
    allowed_actions: List[str]
    allowed_directories: List[str]
    max_risk_score: int


# =========================
# SUBMISSION
# =========================

class Submission(BaseModel):
    paper_text: str
    email: str
    malicious_mode: Optional[bool] = False
    user_policy: UserPolicy


# =========================
# AGENT OUTPUTS
# =========================

class AuthorOutput(BaseModel):
    structured_claims: str
    confidence_score: float


class ReviewOutput(BaseModel):
    novelty_score: float
    methodology_score: float
    ethical_flags: List[str]


# =========================
# POLICY RESULT
# =========================

class PolicyResult(BaseModel):
    approved: bool
    violations: List[str]
    risk_score: int
    modified_claims: str
    governance_summary: str
    reasoning_trace: List[str]
    delegation_trace: Optional[List[str]] = []


# =========================
# EXECUTION PLAN
# =========================

class ExecutionPlan(BaseModel):
    action: str
    target_directory: str
    filename: str
    requires_email: Optional[bool] = False
    requires_pdf: Optional[bool] = False


# =========================
# EXECUTION RESULT
# =========================

class ExecutionResult(BaseModel):
    execution_status: str
    file_path: Optional[str]
    pdf_report_path: Optional[str]
    guard_trace: List[str]
    execution_plan: Optional[ExecutionPlan]
    email_notification: Optional[dict]
    red_team_blocked: bool


# =========================
# FINAL RESPONSE
# =========================

class FinalResponse(BaseModel):
    author_output: AuthorOutput
    review_output: ReviewOutput
    policy_result: PolicyResult
    final_decision: str
    execution_result: ExecutionResult
    audit_log: List[str]