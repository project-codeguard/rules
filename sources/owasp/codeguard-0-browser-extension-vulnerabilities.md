---
description: Browser Extension Security Best Practices
languages:
- c
- javascript
- typescript
alwaysApply: false
---

A browser extension can access sensitive user data and modify web page content, making security a top priority. Here are the key areas to focus on when developing extensions.

### 1. The Manifest: Your Security Foundation

Your `manifest.json` file is the heart of your extension's security model. Configure it with the principle of least privilege.

*   **Permissions:** Only request the permissions your extension absolutely needs to function. Avoid broad host permissions like `<all_urls>` or `http://*/*`. If you only need to access a few sites, specify them explicitly.
*   **Content Security Policy (CSP):** Define a strict CSP to mitigate XSS and other injection attacks. A good starting point is:

    ```json
    "content_security_policy": {
      "extension_pages": "script-src 'self'; object-src 'self'"
    }
    ```

    This policy disallows inline scripts and `eval()`, and restricts script and object sources to your extension's own package.

### 2. Secure Coding Practices

*   **Avoid Dynamic Code Execution:** Never use `eval()`, `new Function()`, `setTimeout()` with strings, or dynamic `import()` of remote URLs. These are major security risks.

*   **Sanitize DOM Inputs:** To prevent XSS from content scripts, never use `.innerHTML` with data that isn't fully sanitized. Prefer safer APIs like `.textContent`, or use a trusted library like DOMPurify.

    **Example:**
    ```javascript
    // Insecure:
    document.getElementById('user-greeting').innerHTML = `Welcome, ${userInput}!`;

    // Secure:
    document.getElementById('user-greeting').textContent = `Welcome, ${userInput}!`;
    ```

### 3. Data Storage and Communication

*   **Use `chrome.storage`:** Avoid `localStorage` for storing any sensitive information. `localStorage` is accessible by any script on the same origin, including potentially malicious scripts injected into the page. Use the `chrome.storage` API instead, which is isolated to your extension.
*   **Encrypt Sensitive Data:** Before storing any sensitive user data, encrypt it.
*   **Use HTTPS:** All network communication must use HTTPS (`wss://` for WebSockets) to protect data in transit. Monitor network requests to prevent unauthorized data exfiltration.

### 4. Interacting with Web Pages

*   **Isolate Sensitive UI:** Do not inject sensitive information directly into a web page's DOM. A malicious script on the page could scrape this data. Instead, display sensitive information in extension-owned UI elements like popups, sidebars, or options pages.
*   **Use Message Passing:** Use the standard message passing APIs (`chrome.runtime.sendMessage`, `chrome.tabs.sendMessage`) for communication between your content scripts and background scripts. Do not use the DOM as a communication channel.

### 5. Supply Chain Security

*   **Audit Dependencies:** Regularly audit your third-party libraries using tools like `npm audit`. A malicious or vulnerable dependency can compromise your entire extension.
*   **No Remote Code:** Do not fetch and execute remote code. All of your extension's logic should be included in its initial package. This is a requirement for most browser extension marketplaces.