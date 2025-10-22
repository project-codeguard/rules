---
description: Authorization Security Best Practices
languages:
- c
- go
- java
- javascript
- php
- python
- ruby
- typescript
- yaml
alwaysApply: false
---

Implementing robust authorization is critical to ensure users can only access the data and features they are permitted to. While authentication confirms who a user is, authorization determines what they can do.

### Core Principles of Secure Authorization

1.  **Deny by Default:** The default for any access request should be 'deny'. Explicitly grant permissions to roles or users rather than explicitly denying them. When no allow rule matches, return HTTP 403 Forbidden.
2.  **Principle of Least Privilege:** Grant users the minimum level of access required to perform their job functions. Regularly audit permissions to ensure they are not excessive.
3.  **Validate Permissions on Every Request:** Check authorization for every single request, regardless of source (AJAX, API, direct). Use middleware/filters to ensure consistent enforcement.
4.  **Prefer ABAC/ReBAC over RBAC:** Use Attribute-Based Access Control (ABAC) or Relationship-Based Access Control (ReBAC) for fine-grained permissions instead of simple role-based access control.

### Server-Side Enforcement is Non-Negotiable

All authorization decisions must be enforced on the server-side for every request. Client-side checks are for user experience only and can be easily bypassed.

**What to Avoid (Anti-Pattern):**

```javascript
// Insecure: Client-side check that can be bypassed by an attacker.
if (currentUser.isAdmin) {
  showAdminDashboard();
} // The server must also check if the user is an admin before returning data.
```

**Best Practice:**

Use centralized middleware or decorators in your backend framework to enforce authorization checks consistently across all relevant endpoints.

**Example (Express.js middleware showing deny-by-default):**

```javascript
function canViewProject(req, res, next) {
  const project = await db.getProject(req.params.id);

  // Explicit allow conditions
  if (project.ownerId === req.user.id) {
    return next(); // Owner can view
  }
  if (req.user.isAdmin) {
    return next(); // Admin can view
  }
  if (project.isPublic && req.user.isVerified) {
    return next(); // Verified users can view public projects
  }

  // Deny by default - no allow rule matched
  return res.status(403).json({
    error: 'Access denied',
    message: 'You do not have permission to view this resource'
  });
}

app.get('/projects/:id', isAuthenticated, canViewProject, (req, res) => {
  // return project data
});
```

### Prevent Insecure Direct Object References (IDOR)

An IDOR vulnerability occurs when an application uses a user-supplied identifier (like a database ID) to access an object directly, without verifying the user has permission to access *that specific object*.

**What to Avoid (Anti-Pattern):**

```javascript
// Insecure: The code checks if the user is authenticated, but not if they
// are authorized to view the invoice with the given ID.
app.get('/invoices/:id', isAuthenticated, (req, res) => {
  const invoice = await db.getInvoice(req.params.id); // Attacker can cycle through IDs
  res.json(invoice);
});
```

**Best Practice:**

Always verify that the authenticated user has the necessary permissions for the specific object they are requesting.

### Additional Best Practices

*   **Token Lifecycle Management:** Implement token revocation for logout/role changes and session invalidation when permissions change.
*   **Centralized Error Handling:** Return generic error messages (403 Forbidden or 404 Not Found) when authorization fails to avoid information leakage.
*   **Comprehensive Logging:** Log all authorization failures with user ID, resource, action, and timestamp for security monitoring.
*   **Testing:** Write unit and integration tests for authorization logic. Test both positive (should have access) and negative (should be denied) cases.
*   **Static Resources:** Apply authorization checks to static files, cloud storage, and other resources, not just API endpoints.