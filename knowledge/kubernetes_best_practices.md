# Kubernetes Security Best Practices
# Source: CIS Kubernetes Benchmark + NSA/CISA Kubernetes Hardening Guide (summary for local RAG)

## Pod Security
- Never run containers as root; set `runAsNonRoot: true` in securityContext.
- Set `readOnlyRootFilesystem: true` to prevent runtime filesystem modifications.
- Disable privilege escalation with `allowPrivilegeEscalation: false`.
- Drop all Linux capabilities and add back only those required.
- Avoid `privileged: true` containers — they bypass all kernel security restrictions.
- Use Pod Security Standards (Restricted) to enforce baseline security.

## Image Security
- Never use the `latest` tag; always pin to specific image digests or version tags.
- Use trusted, minimal base images (distroless or Alpine).
- Scan container images with Trivy or Snyk before deployment.
- Use private registries with authenticated pull secrets.
- Enable image signing and verification (Cosign / Notary).

## Network Policies
- Default-deny all ingress and egress traffic with a baseline NetworkPolicy.
- Apply NetworkPolicies to limit pod-to-pod communication to only what is required.
- Use Calico or Cilium for policy enforcement with eBPF visibility.
- Segment workloads into separate namespaces by environment (prod, staging, dev).

## RBAC and Access Control
- Follow principle of least privilege for ServiceAccounts.
- Disable automounting of ServiceAccount tokens unless explicitly needed.
- Avoid cluster-admin role bindings; use namespace-scoped roles instead.
- Audit RBAC with `kubectl auth can-i --list` regularly.
- Rotate ServiceAccount tokens and use short-lived credentials.

## Secrets Management
- Never store secrets in ConfigMaps or environment variables in plain text.
- Use Kubernetes Secrets with etcd encryption at rest.
- Prefer external secret managers (AWS Secrets Manager, HashiCorp Vault) via CSI driver.
- Rotate secrets regularly and audit access with audit logging.

## Resource Management
- Always define CPU and memory `requests` and `limits` for all containers.
- Use LimitRange and ResourceQuota to enforce resource governance per namespace.
- Monitor resource usage with kube-state-metrics and Prometheus.

## Cluster Configuration
- Enable etcd encryption at rest for all Kubernetes secrets.
- Enable audit logging on the API server.
- Use a managed Kubernetes service (EKS, GKE, AKS) to reduce control plane attack surface.
- Keep Kubernetes versions up to date; patch within 30 days of CVE disclosure.
- Restrict API server access to known IP ranges using allowlists.

## Observability
- Deploy Prometheus + Grafana for cluster metrics and alerting.
- Use OpenTelemetry for distributed tracing across microservices.
- Enable Falco for runtime threat detection (abnormal syscalls).
- Centralise logs using FluentBit → CloudWatch Logs or OpenSearch.
