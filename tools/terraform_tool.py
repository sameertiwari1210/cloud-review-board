def run_terraform_analysis(tf_code: str) -> str:
    """Simple static analysis for Terraform code.

    Checks for:
    - Open CIDR blocks (0.0.0.0/0)
    - Missing encryption settings
    - Missing tags
    - Publicly exposed resources
    Returns a bullet‑point string of findings.
    """
    findings = []
    if "0.0.0.0/0" in tf_code:
        findings.append("- Detected open CIDR block (0.0.0.0/0); this may expose resources publicly.")
    if "encryption" not in tf_code.lower():
        findings.append("- Encryption not configured; consider enabling at rest encryption for storage resources.")
    if "tags" not in tf_code.lower():
        findings.append("- No tags found; tagging resources aids cost allocation and security tracking.")
    if "public = true" in tf_code.lower():
        findings.append("- Resource marked as public; evaluate if this is required.")
    if not findings:
        return "- No obvious security issues detected in the Terraform code."
    return "\n".join(findings)
