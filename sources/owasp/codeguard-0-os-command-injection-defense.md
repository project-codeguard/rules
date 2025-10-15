---
description: OS Command Injection Defense
languages:
- c
- go
- java
- javascript
- perl
- php
- python
- ruby
- shell
alwaysApply: false
version: 0.1.0
severity: medium
---

## OS Command Injection Defense Guidelines

Essential practices for preventing OS command injection vulnerabilities when executing system commands in applications.

### Understanding Command Injection

Command injection occurs when software constructs a system command using externally influenced input without properly neutralizing special elements that can modify the intended command.

Example of vulnerable input:
```
calc & echo "test"
```

This changes the meaning from executing just `calc` to executing both `calc` and `echo "test"`.

#### Argument Injection

Every OS Command Injection is also an Argument Injection, where user input can be passed as arguments while executing a specific command. For example:

```php
system("curl " . escape("--help"))
```

Even with escaping, this shows the output of `curl --help` instead of the intended behavior.

### Primary Defenses

#### Defense Option 1: Avoid Calling OS Commands Directly

The primary defense is to avoid calling OS commands directly. Built-in library functions are preferred as they cannot be manipulated to perform unintended tasks.

Example: Use `mkdir()` instead of `system("mkdir /dir_name")`.

#### Defense Option 2: Escape Values Added to OS Commands

Use language-specific escaping functions when OS commands cannot be avoided.

PHP example using escapeshellarg():
The `escapeshellarg()` function surrounds user input in single quotes, so malformed input like `& echo "hello"` becomes `calc '& echo "hello"'` which is parsed as a single argument.

Note: Even with `escapeshellarg()`, an attacker can still pass a single argument to the command.

#### Defense Option 3: Parameterization with Input Validation

If system commands incorporating user input cannot be avoided, use two layers of defense:

Layer 1 - Parameterization:
Use structured mechanisms that automatically enforce separation between data and command, providing proper quoting and encoding.

Layer 2 - Input Validation:
- Commands: Validate against a list of allowed commands
- Arguments: Use positive/allowlist input validation where arguments are explicitly defined
- Allowlist Regular Expression: Define allowed characters and maximum length, excluding metacharacters

Example regex allowing only lowercase letters and numbers (3-10 characters): `^[a-z0-9]{3,10}$`

POSIX Guideline: Use `--` delimiter to prevent argument injection:
```
curl -- $url
```
This prevents argument injection even if `$url` contains additional arguments.

Dangerous metacharacters to avoid:
```
& |  ; $ > < ` \ ! ' " ( )
```

### Code Examples

#### Java

Use ProcessBuilder with separated command and arguments:

Incorrect usage:
```java
ProcessBuilder b = new ProcessBuilder("C:\DoStuff.exe -arg1 -arg2");
```

Correct usage:
```java
ProcessBuilder pb = new ProcessBuilder("TrustedCmd", "TrustedArg1", "TrustedArg2");

Map<String, String> env = pb.environment();

pb.directory(new File("TrustedDir"));

Process p = pb.start();
```

Note about Runtime.exec:
Java's `Runtime.exec` does NOT invoke the shell and does not support shell metacharacters. It splits strings into arrays and executes the first word with the rest as parameters, making shell-based attacks ineffective.


#### PHP

Use escapeshellarg() or escapeshellcmd() rather than exec(), system(), or passthru().

### Additional Defenses

Implement defense in depth:
- Applications should run with the lowest privileges required for necessary tasks
- Create isolated accounts with limited privileges for single tasks

### Implementation Summary

Secure command execution requires:
- Avoiding OS commands when possible (use built-in libraries)
- Using parameterized execution with separated commands and arguments
- Implementing strict input validation with allowlists
- Applying proper escaping functions when available
- Running applications with minimal privileges
- Using structured mechanisms that enforce data/command separation

Following these practices significantly reduces the risk of OS command injection vulnerabilities in applications.