---
description: Mass Assignment Prevention
languages:
- c
- java
- javascript
- php
- ruby
- scala
alwaysApply: false
version: 0.1.0
severity: medium
---

## Mass Assignment Prevention Guidelines

Essential practices for preventing mass assignment vulnerabilities that allow attackers to modify unintended object properties.

### Understanding Mass Assignment

Mass assignment occurs when frameworks automatically bind HTTP request parameters to program variables or objects. Attackers can exploit this by creating new parameters to overwrite sensitive fields like `isAdmin` or other privilege-related properties.

**Alternative Names by Framework:**
- Mass Assignment: Ruby on Rails, NodeJS
- Autobinding: Spring MVC, ASP NET MVC  
- Object injection: PHP

### Vulnerable Example

User form with typical fields:
```html
<form>
     <input name="userid" type="text">
     <input name="password" type="text">
     <input name="email" text="text">
     <input type="submit">
</form>
```

User object with sensitive field:
```java
public class User {
   private String userid;
   private String password;
   private String email;
   private boolean isAdmin;
   //Getters & Setters
}
```

Vulnerable controller with automatic binding:
```java
@RequestMapping(value = "/addUser", method = RequestMethod.POST)
public String submit(User user) {
   userService.add(user);
   return "successPage";
}
```

Attack payload:
```text
POST /addUser
userid=bobbytables&password=hashedpass&email=bobby@tables.com&isAdmin=true
```

### Primary Defense Strategies

**1. Use Data Transfer Objects (DTOs)**
Create objects exposing only safe, editable fields:

```java
public class UserRegistrationFormDTO {
 private String userid;
 private String password;
 private String email;
 //NOTE: isAdmin field is not present
 //Getters & Setters
}
```

**2. Allow-list Approach**
Explicitly define permitted fields for binding.

**3. Block-list Approach**  
Explicitly exclude sensitive fields from binding.

### Framework-Specific Implementations

#### Spring MVC

Allow-listing permitted fields:
```java
@Controller
public class UserController {
    @InitBinder
    public void initBinder(WebDataBinder binder, WebRequest request) {
        binder.setAllowedFields(["userid","password","email"]);
    }
}
```

Block-listing sensitive fields:
```java
@Controller
public class UserController {
   @InitBinder
   public void initBinder(WebDataBinder binder, WebRequest request) {
      binder.setDisallowedFields(["isAdmin"]);
   }
}
```

#### NodeJS + Mongoose

Allow-listing with underscore.js:
```javascript
var UserSchema = new mongoose.Schema({
    userid: String,
    password: String,
    email : String,
    isAdmin : Boolean,
});

UserSchema.statics = {
    User.userCreateSafeFields: ['userid', 'password', 'email']
};

var User = mongoose.model('User', UserSchema);

_ = require('underscore');
var user = new User(_.pick(req.body, User.userCreateSafeFields));
```

Block-listing with mongoose-mass-assign plugin:
```javascript
var massAssign = require('mongoose-mass-assign');

var UserSchema = new mongoose.Schema({
    userid: String,
    password: String,
    email : String,
    isAdmin : { type: Boolean, protect: true, default: false }
});

UserSchema.plugin(massAssign);
var User = mongoose.model('User', UserSchema);

var user = User.massAssign(req.body);
```

#### PHP Laravel + Eloquent

Allow-listing with $fillable:
```php
<?php
namespace App;
use Illuminate\Database\Eloquent\Model;

class User extends Model {
    private $userid;
    private $password;
    private $email;
    private $isAdmin;

    protected $fillable = array('userid','password','email');
}
```

Block-listing with $guarded:
```php
<?php
namespace App;
use Illuminate\Database\Eloquent\Model;

class User extends Model {
    private $userid;
    private $password;
    private $email;
    private $isAdmin;

    protected $guarded = array('isAdmin');
}
```

### Exploitability Conditions

Mass assignment becomes exploitable when:
- Attacker can guess common sensitive fields
- Attacker has access to source code to review models
- The target object has an empty constructor

### Key Prevention Principles

1. Never bind user input directly to domain objects with sensitive fields
2. Use DTOs to expose only safe, editable fields
3. Apply framework-specific allow-listing or block-listing mechanisms
4. Regularly review models for sensitive attributes
5. Prefer allow-listing over block-listing when possible

Mass assignment protection is critical to prevent unauthorized privilege escalation and data manipulation attacks.