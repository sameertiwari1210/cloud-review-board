# CIS Benchmarks — Cloud Security Controls Summary
# Source: CIS AWS Foundations Benchmark v1.5 (summary for local RAG)

## Identity and Access Management (IAM)
- Avoid the use of the root account; use IAM users or SSO instead.
- Ensure MFA is enabled for all IAM users with console access.
- Ensure credentials unused for 90+ days are disabled.
- Ensure no root account access keys exist.
- Ensure IAM password policy requires at least 14 characters.
- Ensure IAM policies are attached only to groups or roles, not directly to users.
- Ensure access keys are rotated every 90 days or less.

## Logging and Monitoring
- Ensure CloudTrail is enabled in all regions.
- Ensure CloudTrail log file validation is enabled.
- Ensure CloudTrail logs are encrypted using KMS.
- Ensure S3 bucket for CloudTrail is not publicly accessible.
- Ensure CloudWatch alarms exist for unauthorized API calls.
- Ensure CloudWatch alarms exist for root account login.
- Ensure CloudWatch alarms exist for changes to IAM policies, Security Groups, and NACLs.
- Ensure AWS Config is enabled in all regions.

## Networking
- Ensure no security group allows unrestricted inbound access to port 22 (SSH).
- Ensure no security group allows unrestricted inbound access to port 3389 (RDP).
- Ensure no security group allows 0.0.0.0/0 on any port unless explicitly required.
- Ensure VPC flow logging is enabled for all VPCs.
- Ensure the default VPC security group has no inbound or outbound rules.
- Ensure routing tables for VPC peering are least access.

## Storage
- Ensure S3 buckets are not publicly accessible (Block Public Access enabled).
- Ensure S3 bucket policies do not grant global (anonymous) access.
- Ensure S3 bucket versioning is enabled for critical data.
- Ensure S3 server-side encryption is enabled (SSE-KMS preferred).
- Ensure EBS volumes are encrypted using KMS.
- Ensure RDS instances are not publicly accessible.
- Ensure RDS instances are encrypted at rest.
- Ensure automated backups are enabled for RDS instances.

## EC2 and Compute
- Ensure EC2 instances are not directly exposed to the internet via public IPs.
- Ensure EC2 instances use Instance Metadata Service v2 (IMDSv2).
- Ensure no AMIs are publicly shared without explicit intent.
- Ensure EC2 security groups follow principle of least privilege.
