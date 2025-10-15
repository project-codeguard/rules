---
description: CI/CD Security Best Practices
languages:
- javascript
- powershell
- shell
- xml
- yaml
alwaysApply: false
version: 0.1.0
severity: medium
---

The CI/CD pipeline is the backbone of a software development process. It's also a high-value target for attackers. Securing the pipeline is essential for protecting code, infrastructure, and users.

### 1. Secure Your Source Code

The pipeline starts with your source code repository.

*   **Protected Branches:** Configure protected branches (e.g., `main`, `develop`) in your SCM (GitHub, GitLab, etc.). Require code reviews and passing status checks before any code can be merged.
*   **Commit Signing:** Enforce commit signing (e.g., with GPG keys) to verify the author of every commit and prevent spoofing.

### 2. Don't Hardcode Secrets

Never, ever hardcode secrets (API keys, passwords, tokens) in your pipeline configuration files or source code.

*   **Best Practice:** Use a dedicated secrets management solution (like HashiCorp Vault, AWS Secrets Manager, or your CI platform's built-in secret store). Your pipeline should fetch secrets at runtime. Ensure that secrets are masked and never appear in logs.

    **Example (GitHub Actions):**

    steps:
      - name: Deploy to production
        run: ./deploy.sh
        env:
          API_KEY: ${{ secrets.PROD_API_KEY }} # Fetches from GitHub's encrypted secrets
    ```

### 3. Harden Your Pipeline Configuration

*   **Least Privilege:** Grant the minimum level of permissions necessary to your pipeline's identities and build agents. If a job only needs to build code, it shouldn't have deployment credentials.
*   **Isolated Build Environments:** Use ephemeral, isolated build environments (containers or VMs) that are destroyed after each job to prevent cross-contamination and lateral movement.
*   **Automated Security Scanning:** Integrate security scanning directly into your pipeline. This creates a security gate that prevents vulnerabilities from moving down the line.
    *   **SAST (Static Analysis):** Scans your source code for vulnerabilities.
    *   **SCA (Software Composition Analysis):** Scans your dependencies for known vulnerabilities.
    *   **DAST (Dynamic Analysis):** Scans your running application in a test environment.
    *   **IaC Scanning:** Scans your Infrastructure-as-Code files (Terraform, CloudFormation) for misconfigurations.

### 4. Secure Your Dependencies

Your software is only as secure as its dependencies.

*   **Pin Versions:** Use a lock file (`package-lock.json`, `yarn.lock`, `Gemfile.lock`) to pin your dependencies to specific, trusted versions. This prevents a malicious package from being automatically pulled in.
*   **Validate Integrity:** Use package manager features that validate package integrity using hashes or checksums.
*   **Use Private Registries:** For sensitive internal packages, use a private registry to avoid dependency confusion attacks.

### 5. Sign Everything

To ensure the integrity of your supply chain, cryptographically sign your important assets.

*   **Best Practice:**
    *   Sign your Git commits.
    *   Sign your build artifacts (e.g., Docker images, JAR files).
    *   **Verify signatures** before deployment: ensure all artifacts are signed by trusted keys and reject unsigned or invalidly signed artifacts.
    *   Consider frameworks like **SLSA (Supply-chain Levels for Software Artifacts)** to create a verifiable chain of custody for your software.

By embedding these practices into your daily workflow, you can build a CI/CD pipeline that is not only fast and efficient but also secure and resilient.