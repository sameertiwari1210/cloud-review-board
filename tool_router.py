# ==============================================================================
# Tool Router — Phase 4
# ==============================================================================
# Why: Detects which static analysis tool should run based on keywords in the
#      user prompt and optionally a content string (e.g., pasted Terraform code).
#      Keeps tool invocation logic separate from main.py for clarity.
# Inputs: prompt (str) — the raw user query.
#         content (str) — optional code/text body the user provided.
# Outputs: str — combined tool findings, or empty string if no tool matched.

from datetime import datetime
from tools.terraform_tool import run_terraform_analysis
from tools.kubernetes_tool import run_k8s_check
from tools.aws_tool import run_aws_check
from tools.architecture_tool import run_architecture_analysis


# Why: Returns the current timestamp for verbose logging.
# Inputs: None
# Outputs: str — formatted timestamp.
def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Why: Inspects the user prompt for technology keywords and dispatches to the
#      matching static analysis tool.  Multiple tools may run if multiple
#      keywords are detected.
# Inputs:
#   - prompt (str): The user's query text used for keyword detection.
#   - content (str): Optional body of code or configuration to analyse.
# Outputs:
#   - str: Concatenated findings from all matched tools, or "" if none.
def route_tools(prompt: str, content: str = "") -> str:
    combined = prompt.lower() + " " + content.lower()
    results = []

    # Terraform keyword detection
    if any(kw in combined for kw in ["terraform", ".tf", "hcl"]):
        print(f"[{_ts()}] [Tool Router] Keyword matched → running Terraform tool.")
        target = content if content.strip() else prompt
        results.append("### Terraform Static Analysis\n" + run_terraform_analysis(target))

    # Kubernetes keyword detection
    if any(kw in combined for kw in ["kubernetes", "k8s", "kubectl", "helm", "pod", "manifest"]):
        print(f"[{_ts()}] [Tool Router] Keyword matched → running Kubernetes tool.")
        target = content if content.strip() else prompt
        results.append(run_k8s_check(target))

    # AWS keyword detection
    if any(kw in combined for kw in ["aws", "amazon", "s3", "ec2", "iam", "vpc", "cloudtrail"]):
        print(f"[{_ts()}] [Tool Router] Keyword matched → running AWS tool.")
        target = content if content.strip() else prompt
        results.append(run_aws_check(target))

    if not results:
        print(f"[{_ts()}] [Tool Router] No tool keywords detected — skipping static analysis.")
        return ""

    return "\n\n".join(results)
