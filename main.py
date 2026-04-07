from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models import Submission, FinalResponse
from agents import author_agent, reviewer_agent
from policy import evaluate_policy
from execution import execute_submission
from chair import chair_decision
from logger import log_event, get_logs
from dashboard import get_dashboard_stats
from database import init_db

# ==========================================
# APP INITIALIZATION
# ==========================================

app = FastAPI()
init_db()

templates = Jinja2Templates(directory="templates")


# ==========================================
# HOME ROUTE
# ==========================================

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


# ==========================================
# SUBMISSION PIPELINE
# ==========================================

@app.post("/submit", response_model=FinalResponse)
def submit_paper(submission: Submission):

    try:
        log_event("Submission received")

        # -------------------------
        # Author Agent
        # -------------------------
        author_output = author_agent(submission)
        log_event("Author agent processed submission")

        # -------------------------
        # Reviewer Agent
        # -------------------------
        review_output = reviewer_agent(submission)
        log_event("Reviewer agent evaluated submission")

        # -------------------------
        # Policy Engine
        # -------------------------
        policy_result = evaluate_policy(author_output, review_output)
        log_event("Policy evaluation completed")

        # -------------------------
        # Chair Decision
        # -------------------------
        decision = chair_decision(policy_result)
        log_event(f"Chair decision: {decision}")

        # -------------------------
        # Execution Layer
        # -------------------------
        execution_result = execute_submission(
            decision,
            submission,
            policy_result
        )

        log_event("Execution layer completed")

        return FinalResponse(
            author_output=author_output,
            review_output=review_output,
            policy_result=policy_result,
            final_decision=decision,
            execution_result=execution_result,
            audit_log=get_logs()
        )

    except Exception as e:
        log_event(f"ERROR: {str(e)}")
        raise e


# ==========================================
# DASHBOARD ROUTE
# ==========================================

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    try:
        stats = get_dashboard_stats()

        return templates.TemplateResponse(request, "dashboard.html", {
            "stats": stats
        })

    except Exception as e:
        log_event(f"Dashboard error: {str(e)}")
        return HTMLResponse(
            content=f"<h2>Dashboard Error</h2><p>{str(e)}</p>",
            status_code=500
        )