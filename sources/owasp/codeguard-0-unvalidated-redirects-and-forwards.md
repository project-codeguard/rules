---
description: Unvalidated Redirects and Forwards Prevention
languages:
- c
- java
- javascript
- php
- ruby
- rust
- typescript
alwaysApply: false
---

## Unvalidated Redirects and Forwards Prevention

Prevent open redirect and forward vulnerabilities by validating all user-controlled redirect destinations to stop phishing attacks and access control bypass.

### Security Risks

Unvalidated redirects and forwards occur when applications accept untrusted input for redirect destinations, enabling:
- Phishing attacks by redirecting users to malicious sites while maintaining trusted domain appearance
- Access control bypass by forwarding to privileged functions normally restricted
- User credential theft through convincing redirect to attacker-controlled sites

### Safe Redirect Examples

Secure redirects use hardcoded URLs that cannot be manipulated by attackers:

Java:
```java
response.sendRedirect("http://www.mysite.com");
```

PHP:
```php
<?php
/* Redirect browser */
header("Location: http://www.mysite.com");
/* Exit to prevent the rest of the code from executing */
exit;
?>
```

ASP .NET:
```csharp
Response.Redirect("~/folder/Login.aspx")
```

Rails:
```ruby
redirect_to login_path
```

Rust actix web:
```rust
  Ok(HttpResponse::Found()
        .insert_header((header::LOCATION, "https://mysite.com/"))
        .finish())
```

### Dangerous Redirect Examples

Vulnerable code accepts user input directly for redirect destinations:

Java:
```java
response.sendRedirect(request.getParameter("url"));
```

PHP:
```php
$redirect_url = $_GET['url'];
header("Location: " . $redirect_url);
```

C# .NET:
```csharp
string url = request.QueryString["url"];
Response.Redirect(url);
```

Rails:
```ruby
redirect_to params[:url]
```

Rust actix web:
```rust
  Ok(HttpResponse::Found()
        .insert_header((header::LOCATION, query_string.path.as_str()))
        .finish())
```

ASP.NET MVC vulnerable example:
```csharp
[HttpPost]
 public ActionResult LogOn(LogOnModel model, string returnUrl)
 {
   if (ModelState.IsValid)
   {
     if (MembershipService.ValidateUser(model.UserName, model.Password))
     {
       FormsService.SignIn(model.UserName, model.RememberMe);
       if (!String.IsNullOrEmpty(returnUrl))
       {
         return Redirect(returnUrl);
       }
       else
       {
         return RedirectToAction("Index", "Home");
       }
     }
     else
     {
       ModelState.AddModelError("", "The user name or password provided is incorrect.");
     }
   }

   // If we got this far, something failed, redisplay form
   return View(model);
 }
```

Attack example:
```text
 http://example.com/example.php?url=http://malicious.example.com
```

### Dangerous Forward Examples

Server-side forwards can bypass access controls when user input determines the forward destination:

Java servlet vulnerable forward:
```java
public class ForwardServlet extends HttpServlet
{
  protected void doGet(HttpServletRequest request, HttpServletResponse response)
                    throws ServletException, IOException {
    String query = request.getQueryString();
    if (query.contains("fwd"))
    {
      String fwd = request.getParameter("fwd");
      try
      {
        request.getRequestDispatcher(fwd).forward(request, response);
      }
      catch (ServletException e)
      {
        e.printStackTrace();
      }
    }
  }
}
```

Attack example:
```text
http://www.example.com/function.jsp?fwd=admin.jsp
```

### Prevention Strategies

#### Avoid User Input for Destinations
Simply avoid using redirects and forwards, or do not allow URLs as user input for destinations.

#### Use Server-Side Mapping
Have users provide short name, ID, or token mapped server-side to full target URL.

Benefits:
- Highest degree of protection against URL tampering
- Prevents direct URL manipulation

Considerations:
- Prevent enumeration vulnerabilities where users cycle through IDs
- Use sufficiently large or complex token spaces

#### Input Validation and Authorization
If user input cannot be avoided:
- Ensure supplied value is valid and appropriate for the application
- Verify user is authorized for the redirect/forward target
- Validate before performing redirect or forward

#### Allow-List Approach
Create and enforce list of trusted URLs or hosts:
- Use allow-list approach rather than deny-list
- Sanitize input against trusted URL list
- Consider regex patterns for flexible matching

#### External Redirect Warning
Force external redirects through interstitial warning page:
- Clearly display destination to users
- Require user confirmation before proceeding
- Helps users identify potential phishing attempts

#### Framework-Specific Considerations

PHP:
- Always follow header("Location: ...") with exit; to stop execution
- Prevents continued code execution after redirect

ASP.NET MVC:
- MVC 1 & 2 particularly vulnerable to open redirection attacks
- Use MVC 3 or later to avoid vulnerabilities

### Implementation Guidelines

1. Use hardcoded URLs for redirects whenever possible
2. Implement server-side mapping for user-controlled redirects
3. Validate all user input against allow-list of permitted destinations
4. Verify user authorization before performing redirects or forwards
5. Use interstitial warnings for external redirects
6. Follow framework-specific security practices
7. Prevent enumeration through complex token spaces
8. Keep frameworks updated with security patches
9. Never trust user input for determining redirect destinations
10. Test redirect functionality for bypass attempts