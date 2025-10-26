---
description: Laravel Security Best Practices
languages:
- c
- javascript
- php
- typescript
- yaml
alwaysApply: false
---

## Laravel Security Guidelines

Essential security practices for building secure Laravel applications.

### Basic Configuration

Disable debug mode in production and generate application key:

```ini
APP_DEBUG=false
```

```bash
php artisan key:generate
```

Set secure file permissions: directories `775`, files `664`, executables `775`.

### Cookie Security and Session Management

Enable cookie encryption middleware in `App\Http\Kernel`:

```php
protected $middlewareGroups = [
    'web' => [
        \App\Http\Middleware\EncryptCookies::class,
        ...
    ],
    ...
];
```

Configure secure session settings in `config/session.php`:

```php
'http_only' => true,
'domain' => null,
'same_site' => 'lax',
'secure' => null,
'lifetime' => 15,
```

### Mass Assignment Protection

Protect against mass assignment vulnerabilities:

```php
// VULNERABLE: Allows modification of any field
Route::any('/profile', function (Request $request) {
    $request->user()->forceFill($request->all())->save();
    return response()->json(compact('user'));
})->middleware('auth');
```

Use `$request->only()` or `$request->validated()` instead of `$request->all()`.

### SQL Injection Prevention

Use Eloquent ORM parameterized queries by default. For raw queries, always use bindings:

```php
// VULNERABLE: No SQL bindings
User::whereRaw('email = "'.$request->input('email').'"')->get();

// SAFE: Using SQL bindings
User::whereRaw('email = ?', [$request->input('email')])->get();

// SAFE: Named bindings
User::whereRaw('email = :email', ['email' => $request->input('email')])->get();
```

Validate column names to prevent column name injection:

```php
$request->validate(['sortBy' => 'in:price,updated_at']);
User::query()->orderBy($request->validated()['sortBy'])->get();
```

### XSS Prevention

Use Blade's automatic escaping for all untrusted data:

```blade
{{-- SAFE: Automatically escaped --}}
{{ request()->input('somedata') }}

{{-- VULNERABLE: Unescaped data --}}
{!! request()->input('somedata') !!}
```

### File Upload Security

Always validate file type and size:

```php
$request->validate([
    'photo' => 'file|size:100|mimes:jpg,bmp,png'
]);
```

Sanitize filenames to prevent path traversal:

```php
Route::post('/upload', function (Request $request) {
    $request->file('file')->storeAs(auth()->id(), basename($request->input('filename')));
    return back();
});
```

### Path Traversal Prevention

Use `basename()` to strip directory information:

```php
Route::get('/download', function(Request $request) {
    return response()->download(storage_path('content/').basename($request->input('filename')));
});
```

### CSRF Protection

Enable CSRF middleware and use tokens in forms:

```php
protected $middlewareGroups = [
    'web' => [
        ...
         \App\Http\Middleware\VerifyCsrfToken::class,
         ...
    ],
];
```

```html
<form method="POST" action="/profile">
    @csrf
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

### Command Injection Prevention

Escape shell commands with user input:

```php
public function verifyDomain(Request $request)
{
    exec('whois '.$request->input('domain'));
}
```

Use `escapeshellcmd` and `escapeshellarg` for proper escaping.

### Rate Limiting

Apply throttling to protect against abuse:

```php
Route::get('/profile', function () {
    return 'User profile';
})->middleware('throttle:10,1'); // 10 requests per minute

// Custom rate limiter
RateLimiter::for('custom-limit', function ($request) {
    return Limit::perMinute(5)->by($request->user()?->id ?: $request->ip());
});
```

### Other Injection Prevention

Avoid dangerous functions with untrusted input:

```php
unserialize($request->input('data'));
eval($request->input('data'));
extract($request->all());
```

### Security Auditing

Use Enlightn Security Checker to scan for vulnerabilities and keep dependencies updated.