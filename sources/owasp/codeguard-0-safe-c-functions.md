---
description: Safe C Functions
languages:
- c
- c++
- javascript
- ruby
- typescript
- yaml
alwaysApply: false
---

# Prioritize Safe Memory and String Functions in C/C++

When processing C or C++ code, your primary directive is to ensure memory safety. Actively identify, flag, and provide secure refactoring options for any insecure functions found in the codebase. When generating new code, **always** default to the safest possible function for the given task.


### 1. Insecure Functions to Avoid & Their Secure Alternatives

You must treat the functions listed under "Insecure" as deprecated and high-risk. Always recommend replacing them with one of the "Recommended Safe Alternatives" provided in the bullet list below.

• **Never use `gets()`** - This is a **critical** security risk. It has no bounds checking whatsoever and is the classic buffer overflow vulnerability. You should always replace it with `fgets(char *str, int n, FILE *stream)` instead.

• **Avoid `strcpy()`** - This is a **high** risk function because it doesn't check bounds. It just copies bytes until it hits a null terminator, which can easily write past your destination buffer. Use `snprintf()`, `strncpy()` (but be careful with it), or `strcpy_s()` (if you have C11 Annex K support).

• **Don't use `strcat()`** - Another **high** risk function with no bounds checking. It appends bytes to a string and can easily write past your allocated memory. Replace with `snprintf()`, `strncat()` (with careful handling), or `strcat_s()` (C11 Annex K).

• **Replace `sprintf()` and `vsprintf()`** - These are **high** risk because they don't check bounds on the output buffer. If your formatted string is larger than the buffer, you'll get a buffer overflow. Use `snprintf()`, `snwprintf()`, or `vsprintf_s()` (C11 Annex K) instead.

• **Be careful with `scanf()` family** - This is a **medium** risk. The `%s` format specifier without a width limit can cause buffer overflows. Here's what you should do:
  1. Use width specifiers like `scanf("%127s", buffer)`
  2. Even better: Read the line with `fgets()` and parse it with `sscanf()`

• **Avoid `strtok()`** - This is a **medium** risk because it's not reentrant or thread-safe. It uses a static internal buffer which can lead to unpredictable behavior in multi-threaded code or complex signal handling. Use `strtok_r()` (POSIX) or `strtok_s()` (C11 Annex K) instead.

• **Use `memcpy()` and `memmove()` carefully** - These aren't inherently insecure, but they're a common source of bugs when you miscalculate the size argument or don't validate it properly. Here's what you should do:
  1. Double-check your size calculations
  2. Prefer `memcpy_s()` (C11 Annex K) when available
  3. Use `memmove()` if source and destination buffers might overlap

### 2. Actionable Implementation Guidelines

#### For New Code Generation:

- **NEVER** generate code that uses `gets()`, `strcpy()`, `strcat()`, or `sprintf()`.

- **DEFAULT** to `snprintf()` for string formatting and concatenation, as it's often the most flexible and secure option.

- **DEFAULT** to `fgets()` for reading string input from files or standard input.


#### For Code Analysis and Refactoring:

1. **Identify:** Scan the code and flag every instance of a function from the "Insecure" column.

2. **Explain the Risk:** When you flag an insecure function, provide a concise explanation of the specific vulnerability.

    - _Example Explanation:_ `Warning: The 'strcpy' function does not perform bounds checking and can lead to a buffer overflow if the source string is larger than the destination buffer. This is a common security vulnerability.`

3. **Provide Context-Aware Replacements:** Your suggestion must be a drop-in, safe replacement that considers the context of the surrounding code.


#### Use Compiler Flags:

Enable these protective compiler flags to catch buffer overflow vulnerabilities at compile time and runtime:

- **Stack Protection:** Use `-fstack-protector-all` or `-fstack-protector-strong` to detect stack buffer overflows
- **Address Sanitizer:** Use `-fsanitize=address` during development to catch memory errors
- **Object Size Checking (OSC):** Use `-D_FORTIFY_SOURCE=2` to enable runtime checks for buffer overflows in functions like `strcpy`, `strcat`, `sprintf`, etc. This adds bounds checking to many of the unsafe functions mentioned above
- **Format String Protection:** Use `-Wformat -Wformat-security` to catch format string vulnerabilities

### 3. Refactoring Examples

Your suggestions should be concrete and actionable.

**Example 1: Replacing `strcpy`**

- **Original Unsafe Code:**

    ```
    char destination[64];
    strcpy(destination, source_string);
    ```

- **Your Suggested Refactoring:**

    ```
    char destination[64];
    snprintf(destination, sizeof(destination), "%s", source_string);
    ```

- **Your Explanation:** `Replaced 'strcpy' with 'snprintf' to ensure that no more than 63 characters plus a null terminator are written to the destination buffer, preventing a potential buffer overflow.`


**Example 2: Correcting `strncpy` Usage**

The `strncpy` function is a common but imperfect replacement. It may not null-terminate the destination buffer. If you must use it or see it used, you must enforce correct handling.

- **Original (Potentially Unsafe) `strncpy`:**

    ```
    // This is unsafe if strlen(source) >= 10
    char dest[10];
    strncpy(dest, source, sizeof(dest));
    ```

- **Your Corrected Suggestion:**

    ```
    char dest[10];
    strncpy(dest, source, sizeof(dest) - 1);
    dest[sizeof(dest) - 1] = '\0';
    ```

- **Your Explanation:** `Added an explicit null termination for 'strncpy'. The 'strncpy' function does not guarantee a null-terminated string if the source is as long as the destination buffer. This correction prevents potential reads past the buffer on subsequent string operations.`


**Example 3: Securing `scanf`**

- **Original Unsafe Code:**

    ```
    char user_name[32];
    printf("Enter your name: ");
    scanf("%s", user_name);
    ```

- **Your Suggested Refactoring:**

    ```
    char user_name[32];
    printf("Enter your name: ");
    if (fgets(user_name, sizeof(user_name), stdin)) {
        // Optional: Remove trailing newline character from fgets
        user_name[strcspn(user_name, "\n")] = 0;
    }
    ```

- **Your Explanation:** `Replaced 'scanf("%s", ...)' with 'fgets()' to read user input. 'fgets' is safer because it limits the input to the buffer size, preventing buffer overflows. The original 'scanf' had no such protection.`

You must always explain how this rule was applied and why it was applied.