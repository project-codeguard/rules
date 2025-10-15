---
description: Kubernetes Security Best Practices
languages:
- javascript
- shell
- yaml
alwaysApply: false
version: 0.1.0
severity: medium
---

## Kubernetes Security Guidelines

Essential security practices for secure Kubernetes cluster deployment and management.

### Host and Component Security

Keep Kubernetes components updated to the latest stable version. The Kubernetes project maintains release branches for the most recent three minor releases with security fixes.

Secure critical components:
- Restrict access to etcd with mutual TLS authentication and firewall isolation
- Use strong credentials between API servers and etcd
- Control network access to sensitive ports (6443 for API server, 2379-2380 for etcd)
- Enable Kubelet authentication and authorization to prevent unauthenticated access

### Build Phase Security

Use approved, scanned container images from trusted registries:
- Store approved images in private registries
- Integrate vulnerability scanning into CI pipeline to block vulnerable images
- Use minimal base images (distroless when possible) to reduce attack surface
- Remove shells and package managers from runtime containers

### Deploy Phase Security

#### Pod Security Configuration

Apply security context to control pod security parameters:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hello-world
spec:
  containers:
  # specification of the pod's containers
  # ...
  # Security Context
  securityContext:
    readOnlyRootFilesystem: true
    runAsNonRoot: true
```

#### Pod Security Standards

Use Pod Security Admission Controller with namespace-level enforcement:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: policy-test
  labels:    
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

Three security profiles available:
- **Privileged**: Unrestricted (system workloads only)
- **Baseline**: Minimally restrictive, prevents known privilege escalations
- **Restricted**: Most restrictive, enforces current pod hardening practices

#### Network Security

Implement network policies to control pod-to-pod communication:

```json
POST /apis/net.alpha.kubernetes.io/v1alpha1/namespaces/tenant-a/networkpolicys
{
  "kind": "NetworkPolicy",
  "metadata": {
    "name": "pol1"
  },
  "spec": {
    "allowIncoming": {
      "from": [{
        "pods": { "segment": "frontend" }
      }],
      "toPorts": [{
        "port": 80,
        "protocol": "TCP"
      }]
    },
    "podSelector": {
      "segment": "backend"
    }
  }
}
```

#### Resource Management

Define resource quotas to prevent DoS attacks:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-resources
spec:
  hard:
    pods: "4"
    requests.cpu: "1"
    requests.memory: 1Gi
    limits.cpu: "2"
    limits.memory: 2Gi
```

### Secrets Management

- Mount secrets as read-only volumes rather than environment variables
- Store secrets separately from images and pods
- Enable encryption at rest for Secret resources in etcd
- Consider external secrets managers for multi-cluster environments

### Runtime Phase Security

#### Monitoring and Detection

Monitor container behavior for security anomalies:
- Shell execution inside containers
- Sensitive file access (e.g., /etc/shadow)
- Unexpected network connections
- Process activity deviations between replicas

#### Audit Logging

Enable Kubernetes audit logging to track API requests:

```json
{
  "kind":"Event",
  "apiVersion":"audit.k8s.io/v1beta1",
  "metadata":{ "creationTimestamp":"2019-08-22T12:00:00Z" },
  "level":"Metadata",
  "timestamp":"2019-08-22T12:00:00Z",
  "auditID":"23bc44ds-2452-242g-fsf2-4242fe3ggfes",
  "stage":"RequestReceived",
  "requestURI":"/api/v1/namespaces/default/persistentvolumeclaims",
  "verb":"list",
  "user": {
    "username":"user@example.org",
    "groups":[ "system:authenticated" ]
  },
  "sourceIPs":[ "172.12.56.1" ]
}
```

### Access Control

- Implement RBAC with least privilege principles
- Use external authentication (OIDC) with multi-factor authentication
- Avoid built-in authentication methods for production clusters
- Secure the Kubernetes Dashboard with authenticating reverse proxy

### Key Security Requirements

- Always run the latest stable Kubernetes version
- Use namespaces to isolate workloads
- Apply security contexts to prevent privileged container execution
- Implement network policies for traffic segmentation
- Enable comprehensive audit logging and monitoring
- Rotate credentials frequently and revoke bootstrap tokens promptly
- Use admission controllers to enforce security policies