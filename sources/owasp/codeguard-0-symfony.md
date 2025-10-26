---
description: Symfony Security Best Practices
languages:
- php
- yaml
alwaysApply: false
---

## Symfony Security Best Practices

Essential security practices for developing secure Symfony applications, covering common vulnerabilities and framework-specific protections.

### Cross-Site Scripting (XSS) Prevention

Use Twig's default `{{ }}` output escaping for all variables. Only use `|raw` filter for trusted content requiring HTML rendering.

```twig
<p>Hello {{name}}</p>
{# if 'name' is '<script>alert('hello!')</script>', Twig will output this:
'<p>Hello &lt;script&gt;alert(&#39;hello!&#39;)&lt;/script&gt;</p>' #}

<p>{{ product.title|raw }}</p>
{# if 'product.title' is 'Lorem <strong>Ipsum</strong>', Twig will output
exactly that instead of 'Lorem &lt;strong&gt;Ipsum&lt;/strong&gt;' #}
```

### CSRF Protection

Symfony Forms include CSRF tokens automatically. For manual handling, use `csrf_token()` and `isCsrfTokenValid()`.

```php
class PostForm extends AbstractType
{
    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults([
            // ... 
            'csrf_protection' => true,  // enable/disable csrf protection for this form
            'csrf_field_name' => '_csrf_token',
            'csrf_token_id'   => 'post_item', // change arbitrary string used to generate
        ]);
    }
}
```

Manual CSRF token handling:
```twig
<form action="{{ url('delete_post', { id: post.id }) }}" method="post">
    <input type="hidden" name="token" value="{{ csrf_token('delete-post') }}">
    <button type="submit">Delete post</button>
</form>
```

```php
class ExampleController extends AbstractController
{
    #[Route('/posts/{id}', methods: ['DELETE'], name: 'delete_post')]
    public function delete(Post $post, Request $request): Response 
    { 
        $token = $request->request->get('token');
        if($this->isCsrfTokenValid($token)) {
            // ...
        }
        // ...
    }
}
```

### SQL Injection Prevention

Use parameterized queries with Doctrine ORM. Never concatenate user input in SQL strings.

```php
// Repository method
$post = $em->getRepository(Post::class)->findOneBy(['id' => $id]);

// DQL with parameters
$query = $em->createQuery("SELECT p FROM App\Entity\Post p WHERE p.id = :id");
$query->setParameter('id', $id);
$post = $query->getSingleResult();

// DBAL Query Builder
$qb = $em->createQueryBuilder();
$post = $qb->select('p')
            ->from('posts','p')
            ->where('id = :id')
            ->setParameter('id', $id)
            ->getQuery()
            ->getSingleResult();
```

### Command Injection Prevention

Avoid `exec()`, `shell_exec()`, `system()` with user input. Use Symfony Filesystem component or native PHP functions.

```php
// Vulnerable example
$filename = $request->request->get('filename');
exec(sprintf('rm %s', $filename));

// Secure alternatives - use native PHP or Symfony Filesystem
unlink($filename);

// Or Symfony Filesystem component
use Symfony\Component\Filesystem\Filesystem;
$filesystem = new Filesystem();
$filesystem->remove($filename);
```

### File Upload Security

Validate file uploads with Symfony Validator constraints. Store files outside public directory with unique names.

```php
class UploadDto
{
    public function __construct(
        #[File(
            maxSize: '1024k',
            mimeTypes: ['application/pdf', 'application/x-pdf'],
        )]
        public readonly UploadedFile $file,
    ){}
}
```

### Directory Traversal Prevention

Use `realpath()` and `basename()` to validate and sanitize file paths.

```php
$storagePath = $this->getParameter('kernel.project_dir') . '/storage';
$filePath = $storagePath . '/' . $filename;

$realBase = realpath($storagePath);
$realPath = realpath($filePath);

if ($realPath === false || !str_starts_with($realPath, $realBase)) {
    //Directory Traversal!
}

// Alternative: strip directory information
$filePath = $storagePath . '/' . basename($filename);
```

### Security Configuration

Configure session security, authentication, and access controls properly.

```yaml
# Session configuration
framework:
    session:
        cookie_httponly: true
        cookie_lifetime: 5
        cookie_samesite: lax
        cookie_secure: auto

# Authentication providers, firewalls, and access control
security:
    providers:
        app_user_provider:
            entity:
                class: App\Entity\User
                property: email
    firewalls:
        dev:
            pattern: ^/(_(profiler|wdt)|css|images|js)/
            security: false
        admin:
            lazy: true
            provider: app_user_provider
            pattern: ^/admin
            custom_authenticator: App\Security\AdminAuthenticator
            logout:
                path: app_logout
                target: app_login
        main:
            lazy: true
            provider: app_user_provider
    access_control:
        - { path: ^/admin, roles: ROLE_ADMIN }
        - { path: ^/login, roles: PUBLIC_ACCESS }
```

### Production Security

- Set `APP_ENV=prod` and disable debug mode
- Run regular security checks: `composer update` and `symfony check:security`
- Use Symfony secrets for sensitive data
- Configure CORS with `nelmio/cors-bundle` (avoid wildcard origins)
- Implement security headers (HSTS, CSP, X-Frame-Options)
- Enforce HTTPS and set proper file permissions