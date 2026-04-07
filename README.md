# 🔐 PolicyGuard AI
### Intent-Aware Autonomous Governance Engine

<p align="center">
  <b>⚖️ Enforce • 🛡️ Secure • 🤖 Govern AI Systems</b><br><br>
  
</p>

---

## 📌 Overview
PolicyGuard AI is an **intent-aware governance engine** designed to regulate autonomous AI systems that perform real-world actions such as file operations, database updates, and API calls.

It ensures every AI action is:
- ✅ Safe  
- ⚖️ Policy-compliant  
- 🛡️ Secure  
- 📊 Fully traceable  

---

## ❗ Problem
Autonomous AI systems can:
- Perform unauthorized actions  
- Modify critical data  
- Access restricted directories  
- Execute malicious instructions  

Traditional rule-based systems lack contextual intelligence, making them insufficient for AI governance.

---

## 💡 Solution
PolicyGuard AI introduces a **multi-layer governance architecture**:
User → AI Agent → Policy Engine → Runtime Guard → System Resources

✔ Intent analysis  
✔ Risk scoring  
✔ Execution planning  
✔ Runtime enforcement  
✔ Logging & auditing  

---

## 🏗️ Architecture

```mermaid
flowchart LR
    A[User Input] --> B[Agent Layer]
    B --> C[Policy Layer]
    C --> D[Enforcement Layer]
    D --> E[Tool Layer]
    E --> F[Logging & Observability] 
```
⚙️ How It Works
AI input is analyzed
Risk score is computed
Execution plan is generated
Runtime guard validates safety
Action is executed or blocked
Logs and notifications are generated

🔐 Governance Rules
✅ Allowed
Writing to approved directories
Storing metadata in database
Sending notifications after approval

❌ Disallowed
System directory access (e.g., System32)
Unauthorized API calls
Overwriting protected files
Executing OS commands

⚠️ Conditional
Execution allowed only if risk ≤ threshold
Requires policy approval

🛡️ Enforcement
Pre-Execution: Risk validation, policy checks
Runtime: Directory & action validation
Policy-as-Code: Hard constraints (no override)
Logging: Full audit trail

📊 Risk Model
Score	Decision
0	Accept
≤ 3	Minor Revision
≤ 7	Major Revision
> 7	Reject

🔄 Outcomes
✅ Accept → /accepted
✏️ Minor → /minor
⚠️ Major → /major
❌ Reject → /rejected
🚫 Malicious → Blocked

📈 Dashboard
Total submissions
Risk distribution
Average risk score
Activity logs

]## 🖼️ Preview

### 🔹 User Interface
![Interface](screenshots/interface.png)

### 🔹 Accepted Execution Output
![Accept](screenshots/Accept.png)

### 🔹 Major Revision Case
![Major Revision](screenshots/major-revision.png)

### 🔹 Dashboard Overview
![Dashboard](screenshots/dashboard.png)



🧪 Use Cases
AI governance systems
Secure AI pipelines
Enterprise AI compliance
Research validation

🛠️ Tech Stack
Backend: Python
Database: SQLite
AI: LLM integration
Frontend: Dashboard UI
Services: Email notifications

## 🚀 How to Run the Project

### 🔹 Prerequisites
Make sure you have:
- Python (>= 3.8)
- pip
- Git

---

### 🔹 1. Clone the Repository
```bash
git clone https://github.com/ManyaSondhi/PolicyGuard-AI.git
cd PolicyGuard-AI
```
2. Install Dependencies
pip install -r requirements.txt

3.Setup Environment Variables

Create a .env file in the root directory:

EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password

⚠️ Use Gmail App Password (not your real password)

🔹 4. Run the Backend Server
uvicorn main:app --reload

## 👩‍💻 Author
Manya Sondhi
