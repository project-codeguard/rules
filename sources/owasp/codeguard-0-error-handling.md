---
description: Error Handling Security Best Practices
languages:
- c
- java
- javascript
- python
- typescript
- xml
alwaysApply: false
---

## Error Handling Security Guidelines

This rule advises on secure error handling practices to prevent information leakage and ensure proper logging:

- General Error Handling Security
  - Implement global error handlers to catch all unhandled exceptions.
  - Return generic error messages without exposing stack traces, file paths, or version information.
  - Log detailed error information securely on the server side for investigation.
  - Use appropriate HTTP status codes: 4xx for client errors, 5xx for server errors.

- Production Environment Configuration
  - Disable detailed error pages and debug information in production.
  - Set `customErrors mode="RemoteOnly"` in web.config for ASP.NET applications.
  - Disable development exception pages in ASP.NET Core production environments.
  - Configure proper error page redirects to generic error handlers.

- Secure Error Logging
  - Log exceptions with sufficient context (user ID, IP address, timestamp) for forensics.
  - Never log sensitive data like passwords, tokens, or personal information in error logs.
  - Use structured logging for better analysis and monitoring.
  - Implement log rotation and secure storage for error logs.

- Error Response Security
  - Return consistent error response formats using standards like RFC 7807.
  - Add security headers to error responses to prevent XSS and information disclosure.
  - Ensure error response content is properly escaped to prevent injection attacks.
  - Remove server version headers and technology stack information from error responses.

Code Examples (from OWASP):

Standard Java Web Application:
```xml
<!-- web.xml configuration -->
<error-page>
    <exception-type>java.lang.Exception</exception-type>
    <location>/error.jsp</location>
</error-page>
```

```java
<%@ page language="java" isErrorPage="true" contentType="application/json; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%
String errorMessage = exception.getMessage();
//Log the exception via the content of the implicit variable named "exception"
//...
//We build a generic response with a JSON format because we are in a REST API app context
//We also add an HTTP response header to indicate to the client app that the response is an error
response.setHeader("X-ERROR", "true");
//Note that we're using an internal server error response
//In some cases it may be prudent to return 4xx error codes, when we have misbehaving clients
response.setStatus(500);
%>
{"message":"An error occur, please retry"}
```

Spring Boot Global Error Handler:
```java

@RestControllerAdvice
public class RestResponseEntityExceptionHandler extends ResponseEntityExceptionHandler {

    @ExceptionHandler(value = {Exception.class})
    public ProblemDetail handleGlobalError(RuntimeException exception, WebRequest request) {
        //Log the exception via the content of the parameter named "exception"
        //...
        //Note that we're using an internal server error response
        //In some cases it may be prudent to return 4xx error codes, if we have misbehaving clients
        //By specification, the content-type can be "application/problem+json" or "application/problem+xml"
        return ProblemDetail.forStatusAndDetail(HttpStatus.INTERNAL_SERVER_ERROR, "An error occur, please retry");
    }
}
```

ASP.NET Core Error Controller:
```csharp
[Route("api/[controller]")]
[ApiController]
[AllowAnonymous]
public class ErrorController : ControllerBase
{
    [HttpGet]
    [HttpPost]
    [HttpHead]
    [HttpDelete]
    [HttpPut]
    [HttpOptions]
    [HttpPatch]
    public JsonResult Handle()
    {
        //Get the exception that has implied the call to this controller
        Exception exception = HttpContext.Features.Get<IExceptionHandlerFeature>()?.Error;
        //Log the exception via the content of the variable named "exception" if it is not NULL
        //...
        //We build a generic response with a JSON format because we are in a REST API app context
        //We also add an HTTP response header to indicate to the client app that the response is an error
        var responseBody = new Dictionary<String, String>{ {
            "message", "An error occur, please retry"
        } };
        JsonResult response = new JsonResult(responseBody);
        //Note that we're using an internal server error response
        //In some cases it may be prudent to return 4xx error codes, if we have misbehaving clients
        response.StatusCode = (int)HttpStatusCode.InternalServerError;
        Request.HttpContext.Response.Headers.Remove("X-ERROR");
        Request.HttpContext.Response.Headers.Add("X-ERROR", "true");
        return response;
    }
}
```

ASP.NET Web.config Security Configuration:
```xml
<configuration>
    <system.web>
        <customErrors mode="RemoteOnly"
                      defaultRedirect="~/ErrorPages/Oops.aspx" />
    </system.web>
</configuration>
```

Summary:  
Implement centralized error handling with generic user messages while logging detailed error information securely. Disable debug information in production and ensure error responses don't leak sensitive system details.