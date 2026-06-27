# ==============================================================================
# Architecture Static Analysis Tool — Phase 3
# ==============================================================================

# Why: Provides a static text-based analysis of a cloud architecture description
#      without making any network calls. Looks for common architectural weaknesses
#      that a security reviewer should flag.
# Inputs: architecture_text (str) — the raw architecture design text from the LLM.
# Outputs: str — bullet-point findings report.

def run_architecture_analysis(architecture_text: str) -> str:
    """Scan an architecture description for common security and design weaknesses.

    Checks performed (all keyword-based, no network required):
      - Single point of failure (no multi-AZ / redundancy mention)
      - Missing encryption references
      - Missing IAM / access control references
      - Missing logging / audit trail references
      - Missing backup / DR references

    Returns:
        A newline-separated string of bullet-point findings.
    """
    text_lower = architecture_text.lower()
    findings = []

    # --- Single Point of Failure ---
    ha_keywords = ["multi-az", "multi az", "availability zone", "redundan", "failover", "high availability"]
    if not any(kw in text_lower for kw in ha_keywords):
        findings.append(
            "- ⚠️  No high-availability or multi-AZ reference detected. "
            "Ensure the design avoids single points of failure."
        )

    # --- Encryption ---
    if "encrypt" not in text_lower:
        findings.append(
            "- ⚠️  No encryption reference found. "
            "Verify that data at rest and in transit are encrypted."
        )

    # --- IAM / Access Control ---
    iam_keywords = ["iam", "role", "access control", "rbac", "least privilege", "permission"]
    if not any(kw in text_lower for kw in iam_keywords):
        findings.append(
            "- ⚠️  No IAM or access control reference found. "
            "Define role-based permissions and principle of least privilege."
        )

    # --- Logging / Audit ---
    log_keywords = ["logging", "cloudtrail", "audit", "monitor", "cloudwatch", "siem"]
    if not any(kw in text_lower for kw in log_keywords):
        findings.append(
            "- ⚠️  No logging or audit trail reference detected. "
            "Enable CloudTrail, CloudWatch, or equivalent."
        )

    # --- Backup / DR ---
    dr_keywords = ["backup", "disaster recovery", "dr ", "rto", "rpo", "snapshot"]
    if not any(kw in text_lower for kw in dr_keywords):
        findings.append(
            "- ⚠️  No backup or disaster recovery reference found. "
            "Define RTO/RPO targets and automated snapshot policies."
        )

    if not findings:
        return "- ✅ Architecture passes all static checks. No obvious weaknesses detected."

    header = "## Architecture Static Analysis Findings\n"
    return header + "\n".join(findings) + "\n"
