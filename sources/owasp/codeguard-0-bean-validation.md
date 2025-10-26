---
description: Bean Validation Security Best Practices
languages:
- java
- xml
alwaysApply: false
---

Using a declarative, centralized approach to validation is crucial for security and maintainability. The Java Bean Validation standard (now Jakarta Validation) and its primary implementation, Hibernate Validator, provide a powerful way to handle this.

### Why Use Bean Validation?

Instead of scattering validation logic throughout your business layer, you define validation rules directly on your domain models (your "beans"). This keeps your validation logic in one place, making it consistent and easy to manage.

### 1. Setting Up Your Project

Add Hibernate Validator to your `pom.xml`:

```xml
<dependency>
    <groupId>org.hibernate.validator</groupId>
    <artifactId>hibernate-validator</artifactId>
    <version>8.0.0.Final</version>
</dependency>
```

If you're using Spring Boot, the `spring-boot-starter-web` dependency includes Hibernate Validator automatically.

### 2. Annotating Your Beans

Apply standard validation annotations directly to the fields of your model classes. **Always combine @NotNull/@NotBlank with @Size constraints for sensitive fields.**

**Example (`UserForm.java`):**
```java
public class UserForm {

    @NotBlank @Size(min = 2, max = 50)
    private String name;

    @NotBlank @Email @Size(max = 254)
    private String email;

    @NotBlank @Size(min = 8, max = 128)
    @Pattern(regexp = "[A-Za-z0-9@#$%^&+=]+")
    private String password;

    // ... getters and setters
}
```

### 3. Triggering Validation

In a web context (like a Spring MVC controller), use the `@Valid` annotation on your model attribute to trigger the validation process automatically.

**Example (Spring Controller):**
```java
@RestController
public class UserController {

    @PostMapping("/register")
    public ResponseEntity<?> register(@Valid @RequestBody UserForm form, BindingResult result) {
        if (result.hasErrors()) {
            logger.warn("Validation failed: {}", result.getFieldErrors());
            return ResponseEntity.badRequest().body(result.getFieldErrors());
        }

        userService.create(form);
        return ResponseEntity.ok("Success");
    }
}
```

### 4. Validating Nested Objects

If your model contains other objects that also need validation, just annotate them with `@Valid`.

**Example:**
```java
public class Order {
    @Valid @NotNull
    private Address shippingAddress;
}
```

### Best Practices Summary

*   **Centralize Rules:** Define validation constraints on your domain models.
*   **Use Standard Annotations:** Leverage the rich set of built-in annotations (`@NotNull`, `@Size`, `@Pattern`, `@Min`, `@Max`, `@Email`, etc.).
*   **Automate with `@Valid`:** Let your framework trigger validation automatically in your controllers.
*   **Handle Errors Gracefully:** Use `BindingResult` to capture validation errors and return a meaningful `400 Bad Request` response. Never expose sensitive system information in error messages.
*   **Create Custom Constraints:** For complex business rules that aren't covered by standard annotations, create your own custom validation constraints.