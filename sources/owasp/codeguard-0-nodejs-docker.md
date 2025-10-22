---
description: Node.js Docker Security Best Practices
languages:
- d
- javascript
alwaysApply: false
---

## Node.js Docker Security Guidelines

Essential security practices for building optimized and secure Node.js Docker images for production deployment.

### Use Explicit and Deterministic Base Images

Always use specific, pinned base image tags to ensure deterministic builds:
- Avoid `FROM node` or `FROM node:latest` which introduces non-deterministic behavior
- Use minimal base images to reduce attack surface and image size
- Pin images with both tag and SHA256 digest for maximum security

Recommended pattern:
```dockerfile
FROM node:lts-alpine@sha256:b2da3316acdc2bec442190a1fe10dc094e7ba4121d029cb32075ff59bb27390a
```

### Install Only Production Dependencies

Use deterministic dependency installation that excludes development packages:
```dockerfile
RUN npm ci --omit=dev
```

This approach:
- Prevents surprises in CI by halting if lockfile deviations exist
- Reduces security risk from development dependencies
- Decreases image size by excluding unnecessary packages

### Optimize for Production Environment

Set the production environment variable to enable framework optimizations:
```dockerfile
ENV NODE_ENV production
```

Many frameworks like Express only enable performance and security optimizations when this variable is set to "production".

### Run as Non-Root User

Follow the principle of least privilege to minimize security risks:
```dockerfile
COPY --chown=node:node . /usr/src/app
USER node
```

The official node images include a least-privileged `node` user. Ensure all copied files are owned by this user to prevent permission issues.

### Handle Process Signals Properly

Use a proper init system to handle process signals correctly:
```dockerfile
RUN apk add dumb-init
CMD ["dumb-init", "node", "server.js"]
```

Avoid these problematic patterns:
- `CMD "npm" "start"` - npm doesn't forward signals
- `CMD "node" "server.js"` - Node.js as PID 1 doesn't handle signals properly

### Implement Graceful Shutdown

Add signal handlers in your Node.js application code:
```javascript
    async function closeGracefully(signal) {
       console.log(`*^!@4=> Received signal to terminate: ${signal}`)
     
       await fastify.close()
       // await db.close() if we have a db connection in this app
       // await other things we should cleanup nicely
       process.exit()
    }
    process.on('SIGINT', closeGracefully)
    process.on('SIGTERM', closeGracefully)
```

### Use Multi-Stage Builds

Separate build and production stages to minimize final image size and prevent secret leakage:

```dockerfile
# --------------> The build image
FROM node:latest AS build
WORKDIR /usr/src/app
COPY package*.json /usr/src/app/
RUN --mount=type=secret,mode=0644,id=npmrc,target=/usr/src/app/.npmrc npm ci --omit=dev

# --------------> The production image
FROM node:lts-alpine@sha256:b2da3316acdc2bec442190a1fe10dc094e7ba4121d029cb32075ff59bb27390a
RUN apk add dumb-init
ENV NODE_ENV production
USER node
WORKDIR /usr/src/app
COPY --chown=node:node --from=build /usr/src/app/node_modules /usr/src/app/node_modules
COPY --chown=node:node . /usr/src/app
CMD ["dumb-init", "node", "server.js"]
```

### Use .dockerignore File

Create a `.dockerignore` file to exclude unnecessary and sensitive files:
```
node_modules
npm-debug.log
Dockerfile
.git
.gitignore
.npmrc
```

This prevents:
- Copying modified local `node_modules/` over the container-built version
- Including sensitive files like credentials or local configuration
- Cache invalidation from log files or temporary files

### Mount Secrets Securely

Use Docker BuildKit secrets to handle sensitive files like `.npmrc`:
```dockerfile
RUN --mount=type=secret,mode=0644,id=npmrc,target=/usr/src/app/.npmrc npm ci --omit=dev
```

Build command:
```bash
docker build . -t nodejs-tutorial --secret id=npmrc,src=.npmrc
```

This ensures secrets are never copied into the final Docker image layers.

### Security Scanning

Regularly scan your Docker images for vulnerabilities using static analysis tools and keep dependencies updated.

By following these practices, you'll create secure, optimized, and maintainable Node.js Docker images suitable for production deployment.