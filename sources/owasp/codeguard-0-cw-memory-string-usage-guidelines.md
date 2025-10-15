---
description: Memory and String Safety Guidelines
languages:
- c
alwaysApply: false
version: 0.1.0
severity: medium
---

### Memory and String Safety Guidelines

#### Unsafe Memory Functions - FORBIDDEN
**NEVER use these unsafe memory functions that don't check input parameter boundaries:**

##### Banned Memory Functions:
- `memcpy()` → Use `memcpy_s()`
- `memset()` → Use `memset_s()`
- `memmove()` → Use `memmove_s()`
- `memcmp()` → Use `memcmp_s()`
- `bzero()` → Use `memset_s()`
- `memzero()` → Use `memset_s()`

##### Safe Memory Function Replacements:
```c
// Instead of: memcpy(dest, src, count);
errno_t result = memcpy_s(dest, dest_size, src, count);
if (result != 0) {
// Handle error
}

// Instead of: memset(dest, value, count);
errno_t result = memset_s(dest, dest_size, value, count);

// Instead of: memmove(dest, src, count);
errno_t result = memmove_s(dest, dest_size, src, count);

// Instead of: memcmp(s1, s2, count);
int indicator;
errno_t result = memcmp_s(s1, s1max, s2, s2max, count, &indicator);
if (result == 0) {
// indicator contains comparison result: <0, 0, or >0
}
```

#### Unsafe String Functions - FORBIDDEN
**NEVER use these unsafe string functions that can cause buffer overflows:**

##### Banned String Functions:
- `strstr()` → Use `strstr_s()`
- `strtok()` → Use `strtok_s()`
- `strcpy()` → Use `strcpy_s()`
- `strcmp()` → Use `strcmp_s()`
- `strlen()` → Use `strnlen_s()`
- `strcat()` → Use `strcat_s()`
- `sprintf()` → Use `snprintf()`

##### Safe String Function Replacements:
```c
// String Search
errno_t strstr_s(char *dest, rsize_t dmax, const char *src, rsize_t slen, char **substring);

// String Tokenization
char *strtok_s(char *dest, rsize_t *dmax, const char *src, char **ptr);

// String Copy
errno_t strcpy_s(char *dest, rsize_t dmax, const char *src);

// String Compare
errno_t strcmp_s(const char *dest, rsize_t dmax, const char *src, int *indicator);

// String Length (bounded)
rsize_t strnlen_s(const char *str, rsize_t strsz);

// String Concatenation
errno_t strcat_s(char *dest, rsize_t dmax, const char *src);

// Formatted String (always use size-bounded version)
int snprintf(char *s, size_t n, const char *format, ...);
```

#### Implementation Examples:

##### Safe String Copy Pattern:
```c
// Bad - unsafe
char dest[256];
strcpy(dest, src); // Buffer overflow risk!

// Good - safe
char dest[256];
errno_t result = strcpy_s(dest, sizeof(dest), src);
if (result != 0) {
// Handle error: src too long or invalid parameters
EWLC_LOG_ERROR("String copy failed: %d", result);
return ERROR;
}
```

##### Safe String Concatenation Pattern:
```c
// Bad - unsafe
char buffer[256] = "prefix_";
strcat(buffer, suffix); // Buffer overflow risk!

// Good - safe
char buffer[256] = "prefix_";
errno_t result = strcat_s(buffer, sizeof(buffer), suffix);
if (result != 0) {
EWLC_LOG_ERROR("String concatenation failed: %d", result);
return ERROR;
}
```

##### Safe Memory Copy Pattern:
```c
// Bad - unsafe
memcpy(dest, src, size); // No boundary checking!

// Good - safe
errno_t result = memcpy_s(dest, dest_max_size, src, size);
if (result != 0) {
EWLC_LOG_ERROR("Memory copy failed: %d", result);
return ERROR;
}
```

##### Safe String Tokenization Pattern:
```c
// Bad - unsafe
char *token = strtok(str, delim); // Modifies original string unsafely

// Good - safe
char *next_token = NULL;
rsize_t str_max = strnlen_s(str, MAX_STRING_SIZE);
char *token = strtok_s(str, &str_max, delim, &next_token);
while (token != NULL) {
// Process token
token = strtok_s(NULL, &str_max, delim, &next_token);
}
```

#### Memory and String Safety Code Review Checklist:

##### Pre-Code Review (Developer):
- [ ] No unsafe memory functions (`memcpy`, `memset`, `memmove`, `memcmp`, `bzero`)
- [ ] No unsafe string functions (`strcpy`, `strcat`, `strcmp`, `strlen`, `sprintf`, `strstr`, `strtok`)
- [ ] All memory operations use `*_s()` variants with proper size parameters
- [ ] Buffer sizes are correctly calculated using `sizeof()` or known limits
- [ ] No hardcoded buffer sizes that could change

##### Code Review (Reviewer):
- [ ] **Memory Safety**: Verify all memory operations use safe variants
- [ ] **Buffer Bounds**: Confirm destination buffer sizes are properly specified
- [ ] **Error Handling**: Check that all `errno_t` return values are handled
- [ ] **Size Parameters**: Validate that `rsize_t dmax` parameters are correct
- [ ] **String Termination**: Ensure strings are properly null-terminated
- [ ] **Length Validation**: Check that source string lengths are validated before operations

##### Static Analysis Integration:
- [ ] Enable compiler warnings for unsafe function usage
- [ ] Use static analysis tools to detect unsafe function calls
- [ ] Configure build system to treat unsafe function warnings as errors
- [ ] Add pre-commit hooks to scan for banned functions

#### Common Pitfalls and Solutions:

##### Pitfall 1: Wrong Size Parameter
```c
// Wrong - using source size instead of destination size
strcpy_s(dest, strlen(src), src); // WRONG!

// Correct - using destination buffer size
strcpy_s(dest, sizeof(dest), src); // CORRECT
```

##### Pitfall 2: Ignoring Return Values
```c
// Wrong - ignoring potential errors
strcpy_s(dest, sizeof(dest), src); // Error not checked

// Correct - checking return value
if (strcpy_s(dest, sizeof(dest), src) != 0) {
// Handle error appropriately
}
```

##### Pitfall 3: Using sizeof() on Pointers
```c
// Wrong - sizeof pointer, not buffer
void func(char *buffer) {
strcpy_s(buffer, sizeof(buffer), src); // sizeof(char*) = 8!
}

// Correct - pass buffer size as parameter
void func(char *buffer, size_t buffer_size) {
strcpy_s(buffer, buffer_size, src);
}
```