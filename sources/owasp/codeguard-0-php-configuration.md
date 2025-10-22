---
description: PHP Secure Configuration
languages:
- php
alwaysApply: false
---

## PHP Secure Configuration Guidelines

Essential security settings for PHP configuration to harden PHP applications against common vulnerabilities.

### PHP Version Management

Run a supported version of PHP. As of this writing, 8.1 is the oldest version receiving security support from PHP, though distribution vendors often provide extended support.

### Error Handling Configuration

Configure proper error handling to prevent information disclosure while ensuring errors are logged:

```ini
expose_php              = Off
error_reporting         = E_ALL
display_errors          = Off
display_startup_errors  = Off
log_errors              = On
error_log               = /valid_path/PHP-logs/php_error.log
ignore_repeated_errors  = Off
```

Keep `display_errors` to `Off` on production servers and monitor the logs frequently.

### General Security Settings

```ini
doc_root                = /path/DocumentRoot/PHP-scripts/
open_basedir            = /path/DocumentRoot/PHP-scripts/
include_path            = /path/PHP-pear/
extension_dir           = /path/PHP-extensions/
mime_magic.magicfile    = /path/PHP-magic.mime
allow_url_fopen         = Off
allow_url_include       = Off
variables_order         = "GPCS"
allow_webdav_methods    = Off
session.gc_maxlifetime  = 600
```

`allow_url_*` prevents LFIs from being easily escalated to RFIs.

### File Upload Handling

```ini
file_uploads            = On
upload_tmp_dir          = /path/PHP-uploads/
upload_max_filesize     = 2M
max_file_uploads        = 2
```

If your application is not using file uploads, `file_uploads` should be turned `Off`.

### Executable Handling

```ini
enable_dl               = Off
disable_functions       = system, exec, shell_exec, passthru, phpinfo, show_source, highlight_file, popen, proc_open, fopen_with_path, dbmopen, dbase_open, putenv, move_uploaded_file, chdir, mkdir, rmdir, chmod, rename, filepro, filepro_rowcount, filepro_retrieve, posix_mkfifo
disable_classes         =
```

These are dangerous PHP functions. Disable all functions that you don't use.

### Session Handling

Session settings are some of the most important values to concentrate on in configuring. It is a good practice to change `session.name` to something new.

```ini
session.save_path                = /path/PHP-session/
session.name                     = myPHPSESSID
session.auto_start               = Off
session.use_trans_sid            = 0
session.cookie_domain            = full.qualified.domain.name
#session.cookie_path             = /application/path/
session.use_strict_mode          = 1
session.use_cookies              = 1
session.use_only_cookies         = 1
session.cookie_lifetime          = 14400 # 4 hours
session.cookie_secure            = 1
session.cookie_httponly          = 1
session.cookie_samesite          = Strict
session.cache_expire             = 30
session.sid_length               = 256
session.sid_bits_per_character   = 6
```

### Additional Security Settings

```ini
session.referer_check   = /application/path
memory_limit            = 50M
post_max_size           = 20M
max_execution_time      = 60
report_memleaks         = On
html_errors             = Off
zend.exception_ignore_args = On
```

### Advanced Protection with Snuffleupagus

Snuffleupagus is the spiritual descendant of Suhosin for PHP 7 and onwards, with modern features. It's considered stable and is usable in production.

### Implementation Summary

Secure PHP configuration requires:
- Hiding PHP version information (expose_php = Off)
- Proper error handling with logging enabled but display disabled in production
- Disabling remote file access (allow_url_fopen/include = Off)
- Restricting dangerous functions based on application needs
- Hardening session management with secure cookie settings
- Setting appropriate resource limits to prevent DoS
- Using modern security extensions like Snuffleupagus

Following these configuration practices significantly reduces the attack surface of PHP applications and protects against common vulnerabilities.