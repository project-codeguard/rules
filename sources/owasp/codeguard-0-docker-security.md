---
description: Docker Security Best Practices
languages:
- docker
- yaml
alwaysApply: false
version: 0.1.0
severity: medium
---

## Docker Security Guidelines

This rule advises on critical Docker container security practices to protect against common risks:

- Container User Security
  - Always specify a non-root user in Dockerfiles using `USER` directive.
  - Never run containers as root; use `docker run -u <user>` or Kubernetes `securityContext.runAsUser`.
  - Avoid `USER root` or missing `USER` directives in Dockerfiles.

- Docker Daemon Socket Protection
  - DO NOT expose `/var/run/docker.sock` to containers via volume mounts.
  - DO NOT enable TCP Docker daemon socket (`-H tcp://0.0.0.0:XXX`) without TLS.
  - Avoid `- "/var/run/docker.sock:/var/run/docker.sock"` in docker-compose files.

- Capability and Privilege Management
  - Drop all capabilities (`--cap-drop all`) and add only required ones (`--cap-add`).
  - DO NOT use `--privileged` flag in container configurations.
  - Set `allowPrivilegeEscalation: false` in Kubernetes security contexts.
  - Use `--security-opt=no-new-privileges` to prevent privilege escalation.

- Dockerfile Security Practices
  - Pin base image versions (avoid `latest` tags in production).
  - Use `COPY` instead of `ADD` when not extracting archives.
  - DO NOT include secrets, passwords, or API keys in Dockerfiles.
  - Avoid curl bashing in `RUN` directives; use package managers when possible.
  - Include `HEALTHCHECK` instructions for container health monitoring.

- Resource and Filesystem Security
  - Limit container resources (memory, CPU) in docker-compose or Kubernetes specs.
  - Use read-only root filesystems (`--read-only` or `readOnlyRootFilesystem: true`).
  - Mount volumes as read-only (`:ro`) when write access is not needed.
  - Use `--tmpfs` for temporary writable storage instead of persistent volumes.

- Network and Runtime Security
  - Avoid default bridge networking; define custom Docker networks.
  - DO NOT share host network namespace (`--net=host`).
  - DO NOT expose unnecessary ports in Dockerfiles or container configs.
  - Enable default security profiles (seccomp, AppArmor, SELinux); do not disable them.

- Secret Management
  - Use Docker Secrets or Kubernetes encrypted secrets for sensitive data.
  - DO NOT embed secrets in environment variables or Dockerfile layers.
  - Avoid hardcoded credentials in container configurations.

- Container Image Security
  - Scan images for vulnerabilities before deployment.
  - Use minimal base images (alpine, distroless) to reduce attack surface.
  - Remove package managers and unnecessary tools from production images.

Summary:  
Always run containers as non-root users, never expose Docker daemon socket, drop unnecessary capabilities, use secure Dockerfile practices, implement resource limits and read-only filesystems, configure proper networking, manage secrets securely, and scan images for vulnerabilities.