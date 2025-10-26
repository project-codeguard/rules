---
description: Ruby on Rails Security Guidelines
languages:
- c
- javascript
- ruby
- typescript
- yaml
alwaysApply: false
---

## Ruby on Rails Security Guidelines

Essential security practices for developing secure Ruby on Rails applications.

### Command Injection Prevention

Avoid these dangerous methods with user input:

```ruby
eval("ruby code here")
system("os command here")
`ls -al /` # (backticks contain os command)
exec("os command here")
spawn("os command here")
open("| os command here")
Process.exec("os command here")
Process.spawn("os command here")
IO.binread("| os command here")
IO.binwrite("| os command here", "foo")
IO.foreach("| os command here") {}
IO.popen("os command here")
IO.read("| os command here")
IO.readlines("| os command here")
IO.write("| os command here", "foo")
```

Use allowlists and validation when system interaction is necessary.

### SQL Injection Prevention

```ruby
# DANGEROUS - Injectable
name = params[:name]
@projects = Project.where("name like '" + name + "'");

# SAFE - Use parameterized queries
@projects = Project.where("name like ?", "%#{ActiveRecord::Base.sanitize_sql_like(params[:name])}%")
```

### XSS Prevention

Rails auto-escapes by default. Avoid bypassing protection:

```ruby
# DANGEROUS - Do not do this
<%= raw @product.name %>
<%== @product.name %>
<%= @product.name.html_safe %>
```

Use `sanitize` helper for limited HTML with allowed tags only.

### Session Management

Use database-backed sessions for better security:

```ruby
Project::Application.config.session_store :active_record_store
```

### Transport Security

Force HTTPS in production:

```ruby
# config/environments/production.rb
config.force_ssl = true
```

### Authentication with Devise

```bash
gem 'devise'
rails generate devise:install
```

Configure routes:

```ruby
Rails.application.routes.draw do
  authenticate :user do
    resources :something do  # these resource require authentication
      ...
    end
  end

  devise_for :users # sign-up/-in/out routes
  root to: 'static#home' # no authentication required
end
```

Password complexity with zxcvbn:

```ruby
class User < ApplicationRecord
  devise :database_authenticatable,
    # other devise features, then
    :zxcvbnable
end
```

```ruby
# in config/initializers/devise.rb
Devise.setup do |config|
  config.min_password_score = 4 # complexity score here.
  ...
```

### Token Authentication

```bash
gem 'devise_token_auth'
gem 'omniauth'
```

```ruby
mount_devise_token_auth_for 'User', at: 'auth'
```

### CSRF Protection

```ruby
class ApplicationController < ActionController::Base
  protect_from_forgery
```

Token authentication doesn't require CSRF protection.

### Secure Redirects

```ruby
# DANGEROUS
redirect_to params[:url]

# SAFE
begin
  if path = URI.parse(params[:url]).path
    redirect_to path
  end
rescue URI::InvalidURIError
  redirect_to '/'
end
```

Use allowlists for multiple redirect targets:

```ruby
ACCEPTABLE_URLS = {
  'our_app_1' => "https://www.example_commerce_site.com/checkout",
  'our_app_2' => "https://www.example_user_site.com/change_settings"
}

def redirect
  url = ACCEPTABLE_URLS["#{params[:url]}"]
  redirect_to url if url
end
```

### CORS Configuration

```ruby
# Gemfile
gem 'rack-cors', :require => 'rack/cors'

# config/application.rb
module Sample
  class Application < Rails::Application
    config.middleware.use Rack::Cors do
      allow do
        origins 'someserver.example.com'
        resource %r{/users/\d+.json},
        :headers => ['Origin', 'Accept', 'Content-Type'],
        :methods => [:post, :get]
      end
    end
  end
end
```

### Security Headers

```ruby
ActionDispatch::Response.default_headers = {
  'X-Frame-Options' => 'SAMEORIGIN',
  'X-Content-Type-Options' => 'nosniff',
  'X-XSS-Protection' => '0'
}
```

### Sensitive Files Protection

Protect from source control:

```text
/config/database.yml                 -  May contain production credentials.
/config/initializers/secret_token.rb -  Contains a secret used to hash session cookie.
/db/seeds.rb                         -  May contain seed data including bootstrap admin user.
/db/development.sqlite3              -  May contain real data.
```

### Password Hashing

Configure bcrypt stretches:

```ruby
config.stretches = Rails.env.test? ? 1 : 10
```

### Security Testing

Use Brakeman for static analysis:

```bash
gem install brakeman
brakeman -o security_report.html
```

### Key Security Principles

- Never use dangerous command execution methods with user input
- Always use parameterized queries and ActiveRecord methods
- Rely on Rails' automatic HTML escaping
- Use database-backed sessions for sensitive applications
- Enable CSRF protection and validate redirects
- Set security headers and configure CORS carefully
- Maintain secure routing and dependency management
- Regular security testing with Brakeman

Rails provides many security features by default, but developers must use them correctly.