import re

def run_k8s_check(text: str) -> str:
    """Simple rule‑based checks for Kubernetes manifest snippets.

    Returns a markdown report with any findings.
    """
    findings = []
    # Detect usage of image tag "latest"
    if re.search(r"image:\s*['\"]?[^'\"]+[:]?latest['\"]?", text, re.IGNORECASE):
        findings.append("- ⚠️ Container image uses `latest` tag. Pin specific versions.")
    # Detect privileged containers
    if re.search(r"securityContext:\s*{[^}]*privileged:\s*true", text, re.IGNORECASE | re.DOTALL):
        findings.append("- ⚠️ Privileged container detected. Remove privileged flag if not required.")
    # Detect hostPath volumes
    if re.search(r"hostPath:\s*{", text, re.IGNORECASE):
        findings.append("- ⚠️ `hostPath` volume used. Consider using PVCs for better isolation.")
    # Detect missing resource limits/requests
    if re.search(r"resources:\s*{\s*limits:\s*{", text, re.IGNORECASE) is None:
        findings.append("- ⚠️ Resource `limits` not defined. Add CPU/memory limits.")
    if not findings:
        findings.append("- ✅ No immediate Kubernetes security issues found.")
    report = "## Kubernetes Static Review\n" + "\n".join(findings) + "\n"
    return report
