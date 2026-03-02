import json
import sys
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
 
REGRESSION_THRESHOLD = 0.15  # 15% latency increase allowed
 
 
# -------------------------
# Load Metrics
# -------------------------
def load_metrics(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return data["metrics"]
 
 
# -------------------------
# Calculate Percentage Change
# -------------------------
def calculate_change(prev, curr):
    if prev == 0:
        return 0
    return (curr - prev) / prev
 
 
# -------------------------
# Generate AI Summary
# -------------------------
def generate_summary(prev_metrics, curr_metrics):
 
    # Extract required metrics
    prev_p95 = prev_metrics["http_req_duration"]["p(95)"]
    curr_p95 = curr_metrics["http_req_duration"]["p(95)"]
 
    prev_rps = prev_metrics["http_reqs"]["rate"]
    curr_rps = curr_metrics["http_reqs"]["rate"]
 
    prev_error = prev_metrics["http_req_failed"]["value"]
    curr_error = curr_metrics["http_req_failed"]["value"]
 
    # Calculate changes
    p95_change = calculate_change(prev_p95, curr_p95)
    rps_change = calculate_change(prev_rps, curr_rps)
    error_change = calculate_change(prev_error, curr_error)
 
    report = []
    report.append("# AI Performance Summary")
    report.append(f"Generated on: {datetime.now()}\n")
 
    # Regression decision
    if p95_change > REGRESSION_THRESHOLD:
        report.append("Performance Regression Detected\n")
        regression_flag = True
    else:
        report.append("No Performance Regression Detected\n")
        regression_flag = False
 
    # p95 message
    if p95_change < 0:
        report.append(f"- p95 latency decreased by {abs(round(p95_change*100))}%")
    else:
        report.append(f"- p95 latency increased by {round(p95_change*100)}%")
 
    # Throughput message
    if rps_change > 0:
        report.append(f"- Throughput increased by {round(rps_change*100)}%")
    else:
        report.append(f"- Throughput decreased by {abs(round(rps_change*100))}%")
 
    # Error rate message
    if curr_error == prev_error:
        report.append(f"- Error rate stable at {curr_error*100:.0f}%")
    elif curr_error > prev_error:
        report.append(f"- Error rate increased to {curr_error*100:.0f}%")
    else:
        report.append(f"- Error rate decreased to {curr_error*100:.0f}%")
 
    return "\n".join(report), regression_flag
 
 
# -------------------------
# Write Markdown Report
# -------------------------
def write_markdown(content):
    with open("performance_report.md", "w") as f:
        f.write(content)
 
 
# -------------------------
# Generate PDF Report
# -------------------------
def generate_pdf(content):
    doc = SimpleDocTemplate("performance_report.pdf")
    styles = getSampleStyleSheet()
    elements = []
 
    for line in content.split("\n"):
        elements.append(Paragraph(line, styles["Normal"]))
        elements.append(Spacer(1, 6))
 
    doc.build(elements)
 
 
# -------------------------
# Main Execution
# -------------------------
def main():
    prev_metrics = load_metrics("previous.json")
    curr_metrics = load_metrics("results_current.json")
 
    report_content, regression_flag = generate_summary(prev_metrics, curr_metrics)
 
    write_markdown(report_content)
    generate_pdf(report_content)
 
    print(report_content)
 
    # Optional: Fail CI build if regression detected
    if regression_flag:
        sys.exit(1)
 
 
if __name__ == "__main__":
    main()