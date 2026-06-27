import re

def run_aws_check(text: str) -> str:
    """Simple rule‑based checks for AWS configuration snippets.

    Returns a markdown report with any findings.
    """
    findings = []
    # Detect S3 bucket without encryption
    if re.search(r"resource \"aws_s3_bucket\"[^{]*{[^}]*?server_side_encryption_configuration\s*=\s*{\s*}[^}]*}", text, re.IGNORECASE) is None:
        findings.append("- ⚠️ S3 bucket missing server‑side encryption configuration.")
    # Detect security groups with 0.0.0.0/0 ingress
    if re.search(r"ingress\s*{[^}]*cidr_blocks\s*=\s*\[\s*\"0\.0\.0\.0\/0\"\s*\]", text, re.IGNORECASE | re.DOTALL):
        findings.append("- ⚠️ Security group allows ingress from 0.0.0.0/0. Consider restricting source IPs.")
    # Detect IAM role with AdministratorAccess
    if re.search(r"arn:aws:iam::aws:policy/AdministratorAccess", text):
        findings.append("- ⚠️ IAM role attached with `AdministratorAccess` policy. Principle of least privilege violation.")
    if not findings:
        findings.append("- ✅ No immediate AWS configuration security issues found.")
    report = "## AWS Static Review\n" + "\n".join(findings) + "\n"
    return report
