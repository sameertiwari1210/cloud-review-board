# AWS Well-Architected Framework — Key Security & Architecture Principles
# Source: AWS Well-Architected Framework (summary for local RAG)

## Pillar 1: Operational Excellence
- Define operations as code using CloudFormation or CDK.
- Make frequent, small, reversible changes to reduce blast radius.
- Anticipate failure; test recovery procedures regularly.
- Use AWS Systems Manager for patch management and runbooks.

## Pillar 2: Security
- Implement a strong identity foundation using IAM with least privilege.
- Enable traceability with AWS CloudTrail, Config, and Security Hub.
- Apply security at all layers: VPC, subnet, security groups, NACLs, WAF, Shield.
- Protect data in transit using TLS 1.2+ and at rest using KMS-managed keys.
- Prepare for security events with AWS GuardDuty and Macie for threat detection.
- Use AWS Organizations SCPs to enforce guardrails across all accounts.
- Enable MFA for all IAM users, especially the root account.

## Pillar 3: Reliability
- Automatically recover from failure using Auto Scaling and multi-AZ deployments.
- Test recovery procedures with AWS Fault Injection Simulator.
- Scale horizontally to increase aggregate system availability.
- Stop guessing capacity — use Compute Optimizer for right-sizing.
- Manage change through automation using CodePipeline and CodeDeploy.

## Pillar 4: Performance Efficiency
- Use serverless architectures (Lambda, Fargate) to remove server management overhead.
- Use caching (ElastiCache, CloudFront) to reduce latency.
- Deploy globally using Route 53 latency routing and CloudFront edge locations.

## Pillar 5: Cost Optimization
- Implement cloud financial management with AWS Cost Explorer and Budgets.
- Use Savings Plans and Reserved Instances for predictable workloads.
- Select the most cost-effective resource type (Graviton, Spot Instances).
- Delete unused resources; use lifecycle policies for S3 and EBS snapshots.

## Pillar 6: Sustainability
- Maximize utilization of provisioned resources to minimize environmental impact.
- Use managed services that share infrastructure across many customers.

## Key Security Services Reference
| Service | Purpose |
|---|---|
| AWS IAM | Identity and access management |
| AWS KMS | Key management for encryption |
| AWS CloudTrail | API audit logging |
| AWS Config | Resource configuration compliance |
| AWS GuardDuty | Intelligent threat detection |
| AWS Security Hub | Centralised security posture management |
| AWS WAF | Web application firewall |
| AWS Shield | DDoS protection |
| AWS Macie | S3 sensitive data discovery |
| AWS Inspector | Automated vulnerability assessment |
| AWS Secrets Manager | Secrets rotation and storage |
