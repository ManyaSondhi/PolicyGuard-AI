from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


def generate_pdf_report(title, decision, risk_score, violations):

    os.makedirs("reports", exist_ok=True)
    path = os.path.join("reports", "review_report.pdf")

    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(50, 750, "AutoGov-X Review Report")
    c.drawString(50, 730, f"Title: {title}")
    c.drawString(50, 710, f"Decision: {decision}")
    c.drawString(50, 690, f"Risk Score: {risk_score}")

    y = 660
    for v in violations:
        c.drawString(50, y, f"- {v}")
        y -= 20

    c.save()

    return path