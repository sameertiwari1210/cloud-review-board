# Palo Alto Networks — NGFW & Zero Trust Security Practices
# Source: Palo Alto Networks Best Practices (summary for local RAG)

## Next-Generation Firewall (NGFW) Best Practices
- Enable App-ID to identify applications by content, not port — block unknown applications.
- Enable User-ID to tie network traffic to individual users and groups.
- Enable Content-ID (Threat Prevention) for IPS, antivirus, URL filtering, and file blocking.
- Use security zones to segment traffic: Trust, Untrust, DMZ, Management.
- Apply the principle of least privilege in security policies — deny by default.
- Never use Allow Any/Any rules; every rule must have a specific application and user context.
- Enable SSL/TLS Inspection (Decryption) for outbound and inbound encrypted traffic.
- Log all traffic (even allowed) to enable forensic investigation.
- Use WildFire for cloud-based sandbox analysis of unknown files and URLs.
- Enable DNS Security to block DNS-based C2 (command-and-control) communications.

## VM-Series on AWS/Azure/GCP
- Deploy VM-Series in Gateway Load Balancer (GWLB) mode for transparent inline inspection.
- Use Transit Gateway with GWLB to centralize inspection for all VPC traffic.
- Enable HA Active/Passive pairs across Availability Zones for firewall redundancy.
- Use AWS IAM roles for VM-Series bootstrapping — avoid hardcoded credentials.
- Store firewall configuration backups in S3 with SSE-KMS encryption.
- Enable CloudWatch integration for NGFW health metrics and alerting.

## Zero Trust Architecture Principles
- Never trust, always verify — every request must be authenticated and authorized.
- Assume breach; design for containment, not just prevention.
- Verify explicitly using device posture, user identity, and location context.
- Use least-privilege access; just-in-time (JIT) access for privileged operations.
- Micro-segment networks to limit lateral movement after a breach.
- Log and monitor all sessions including internal east-west traffic.

## Prisma Cloud (CSPM/CWPP)
- Enable Cloud Security Posture Management (CSPM) to detect misconfigurations.
- Enable Cloud Workload Protection Platform (CWPP) for runtime container and VM security.
- Integrate Prisma Cloud with CI/CD pipelines for shift-left IaC scanning.
- Use Prisma Cloud policies mapped to CIS, NIST, PCI-DSS, and SOC 2.

## Panorama (Centralized Management)
- Use Panorama to manage all NGFW devices from a single pane of glass.
- Use Device Groups and Templates for consistent policy and configuration deployment.
- Enable role-based administration in Panorama with least privilege.
- Store Panorama configuration backups off-device with version control.
