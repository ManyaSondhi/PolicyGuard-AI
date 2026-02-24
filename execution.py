import os
from datetime import datetime
from models import ExecutionResult, ExecutionPlan
from database import insert_submission
from email_agent import send_email

STORAGE_ROOT = "C:/AutoGovX_Data"


def sanitize_title(text):
    text = text.strip().replace(" ", "_")
    return "".join(c for c in text if c.isalnum() or c in ["_", "-"])[:50]


def generate_versioned_filename(directory, base_name):
    version = 1
    filename = f"{base_name}_v{version}.txt"
    full_path = os.path.join(directory, filename)

    while os.path.exists(full_path):
        version += 1
        filename = f"{base_name}_v{version}.txt"
        full_path = os.path.join(directory, filename)

    return filename


def execute_submission(decision, submission, policy_result):

    guard_trace = []
    user_policy = submission.user_policy

    # =====================================
    # STEP 1 — DETERMINE TARGET DIRECTORY
    # =====================================

    folder_name = "accepted" if decision == "ACCEPT" else "rejected"

    if submission.malicious_mode:
        folder_name = "System32"
        guard_trace.append("Malicious mode activated")

    target_directory = os.path.join(STORAGE_ROOT, folder_name)

    plan = ExecutionPlan(
        action="WRITE_FILE",
        target_directory=target_directory,
        filename="dynamic"
    )

    guard_trace.append("Execution plan generated")

    # =====================================
    # STEP 2 — VALIDATE ACTION
    # =====================================

    if "WRITE_FILE" not in user_policy.allowed_actions:
        guard_trace.append("WRITE_FILE not allowed by policy")
        return ExecutionResult(
            execution_status="BLOCKED",
            file_path=None,
            pdf_report_path=None,
            guard_trace=guard_trace,
            execution_plan=plan,
            email_notification=None,
            red_team_blocked=True
        )

    # 🔥 ONLY CHECK FOLDER NAME NOW
    if folder_name not in [os.path.basename(p) for p in user_policy.allowed_directories]:
        guard_trace.append("Directory not allowed by policy")
        return ExecutionResult(
            execution_status="BLOCKED",
            file_path=None,
            pdf_report_path=None,
            guard_trace=guard_trace,
            execution_plan=plan,
            email_notification=None,
            red_team_blocked=True
        )

    if policy_result.risk_score > user_policy.max_risk_score:
        guard_trace.append("Risk threshold exceeded")
        return ExecutionResult(
            execution_status="BLOCKED",
            file_path=None,
            pdf_report_path=None,
            guard_trace=guard_trace,
            execution_plan=plan,
            email_notification=None,
            red_team_blocked=True
        )

    # =====================================
    # STEP 3 — STORE FILE
    # =====================================

    os.makedirs(target_directory, exist_ok=True)

    title = sanitize_title(submission.paper_text[:30])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"{title}_{timestamp}"

    filename = generate_versioned_filename(target_directory, base_name)
    file_path = os.path.join(target_directory, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(submission.paper_text)

    guard_trace.append("Paper stored successfully")

    # =====================================
    # STEP 4 — LOG TO DATABASE
    # =====================================

    insert_submission(
        title=title,
        decision=decision,
        risk_score=policy_result.risk_score,
        email=submission.email,
        file_path=file_path
    )

    guard_trace.append("Submission logged to database")

    # =====================================
    # STEP 5 — SEND EMAIL
    # =====================================

    email_status = send_email(
        recipient_email=submission.email,
        title=title,
        decision=decision,
        risk_score=policy_result.risk_score
    )

    if email_status:
        guard_trace.append("Email sent successfully")
    else:
        guard_trace.append("Email sending failed")

    # =====================================
    # RETURN RESULT
    # =====================================

    return ExecutionResult(
    execution_status="SUCCESS",
    file_path=file_path,
    pdf_report_path=None,
    guard_trace=guard_trace,
    execution_plan=plan,
    email_notification={
        "recipient": submission.email,
        "status": "SENT" if email_status else "FAILED"
    },
    red_team_blocked=False
)