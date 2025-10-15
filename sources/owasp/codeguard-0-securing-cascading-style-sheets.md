---
description: Securing Cascading Style Sheets
languages:
- c
- javascript
- typescript
alwaysApply: false
version: 0.1.0
severity: medium
---

## Securing Cascading Style Sheets

Prevent CSS files from exposing application features, user roles, and sensitive functionality to attackers performing reconnaissance.

### Security Risks

#### Risk 1: Information Disclosure Through CSS Selectors
Motivated attackers examine CSS files to learn application features before attempting attacks. Global CSS files containing role-based selectors reveal:
- Different user roles and permissions
- Available features and functionality
- Application structure and sensitive endpoints

Example problematic selectors:
- `.profileSettings`
- `.addUsers`
- `.deleteUsers` 
- `.exportUserData`
- `.addNewAdmin`

#### Risk 2: Descriptive Selector Names
Readable selector names help attackers map CSS classes to actual application features:
- `.changePassword`
- `.oldPassword`
- `.newPassword`
- `.confirmNewPassword`

### Defensive Mechanisms

#### Defense 1: Isolate CSS by Access Control Level
- Create separate CSS files per role (StudentStyling.CSS, AdministratorStyling.CSS)
- Restrict CSS file access to users with proper access control level only
- Implement server-side validation before serving CSS files
- Log and alert on unauthorized CSS file access attempts (forced browsing)
- Ensure authenticated users cannot access CSS files for other roles

#### Defense 2: Remove Identifying Information
- Use consistent styling across pages to reduce need for specific selectors
- Write general CSS rules that apply across multiple pages
- Create CSS selectors targeting HTML elements without revealing functionality

Transform descriptive selectors:
```
// Instead of this revealing selector:
#UserPage .Toolbar .addUserButton

// Use obscure structural targeting:
#page_u header button:first-of-type
```

Build-time and runtime obfuscation tools:
- JSS (CSS in JS) with minify option generates class names like `.c001`, `.c002`
- CSS Modules with modules and localIdentName options for obfuscation
- .Net Blazor CSS Isolation creates scoped selectors like `button.add[b-3xxtam6d07]`
- CSS libraries (Bootstrap, Tailwind) reduce need for specific selectors

#### Defense 3: Prevent Malicious CSS in User Content
- Validate and sanitize user-authored HTML content
- Restrict CSS styles allowed in user-generated content
- Prevent uploaded HTML from using styles for unintended purposes
- Be aware that CSS can be used for clickjacking attacks where clicking anywhere on the page loads malicious websites

### Implementation Guidelines

1. Segment CSS files by user roles and access levels
2. Implement access control validation before serving CSS resources
3. Use build-time tools to obfuscate class names and selectors
4. Prefer structural and element-based selectors over feature-specific names
5. Leverage CSS frameworks to minimize custom selectors
6. Sanitize and restrict user-generated HTML content containing styles
7. Monitor and log unauthorized attempts to access role-specific CSS files
8. Avoid global CSS files that contain selectors for all user roles
9. Use generic, non-descriptive class names that don't reveal functionality
10. Test CSS access controls to ensure proper isolation between roles