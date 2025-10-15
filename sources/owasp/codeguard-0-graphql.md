---
description: GraphQL Security Best Practices
languages:
- javascript
- typescript
alwaysApply: false
version: 0.1.0
severity: medium
---

## GraphQL Security Guidelines

This rule advises on secure GraphQL API development to prevent injection, DoS, unauthorized access, and information leakage:

- Input Validation and Injection Prevention
  - Use specific GraphQL data types (scalars, enums) for all input validation.
  - Define custom GraphQL validators for complex validations and use custom scalars.
  - Define schemas for mutation inputs with strict validation rules.
  - Use allowlist approach for character validation (avoid denylists).
  - Apply parameterized statements and safe APIs for database queries in resolvers.
  - Use ORMs/ODMs properly to avoid ORM injection vulnerabilities.
  - Gracefully reject invalid input without revealing internal API details.

- DoS Prevention and Query Limiting
  - Implement query depth limiting using libraries like graphql-depth-limit (JavaScript) or MaxQueryDepthInstrumentation (Java).
  - Add query complexity analysis using graphql-cost-analysis or MaxQueryComplexityInstrumentation.
  - Enforce query amount limiting with libraries like graphql-input-number.
  - Implement pagination to limit data returned in single responses.
  - Add query timeouts at application level using custom instrumentation.
  - Apply rate limiting per IP or user to prevent basic DoS attacks.
  - Use server-side batching and caching (like Facebook's DataLoader) for efficiency.

- Access Control and Authorization
  - Validate requester authorization for all data viewing and mutation operations.
  - Implement proper object-level authorization to prevent IDOR/BOLA vulnerabilities.
  - Enforce authorization checks on both edges and nodes in GraphQL schema.
  - Use Interfaces and Unions to return different object properties based on permissions.
  - Add access control validation in Query and Mutation resolvers with RBAC middleware.
  - Check for unintended node/nodes fields that allow direct object access by ID.
  - Implement field-level access controls for sensitive data.

- Batching Attack Prevention
  - Limit the number of queries that can be batched and run simultaneously.
  - Add object request rate limiting at code level to track instance requests.
  - Prevent batching for sensitive objects (usernames, passwords, tokens, OTPs).
  - Implement custom solutions to disable batching for critical operations.
  - Monitor and log batching attempts for security analysis.

- Secure Configuration Management
  - Disable GraphQL introspection in production environments using NoIntrospectionGraphqlFieldVisibility (Java) or validation rules (JavaScript).
  - Disable GraphiQL and similar exploration tools in production.
  - Configure error masking to prevent stack traces and debug information exposure.
  - Set NODE_ENV to 'production' or use debug: false in Apollo Server configuration.
  - Disable field suggestion hints when introspection is disabled.

- Authentication and Session Management
  - Require authentication for all GraphQL endpoints (unless explicitly public).
  - Implement proper session management with secure token validation.
  - Use JWT or session-based authentication with proper validation in resolvers.
  - Apply CSRF protection for GraphQL mutations when using cookie-based authentication.
  - Validate authentication state before processing any queries or mutations.

Code Examples (from OWASP):

Disable Introspection - Java:
```java
GraphQLSchema schema = GraphQLSchema.newSchema()
    .query(StarWarsSchema.queryType)
    .fieldVisibility( NoIntrospectionGraphqlFieldVisibility.NO_INTROSPECTION_FIELD_VISIBILITY )
    .build();
```

Disable Introspection & GraphiQL - JavaScript:
```javascript
app.use('/graphql', graphqlHTTP({
  schema: MySessionAwareGraphQLSchema,
+ validationRules: [NoIntrospection]
  graphiql: process.env.NODE_ENV === 'development',
}));
```

Query Depth Example:
```javascript
query evil {            # Depth: 0
  album(id: 42) {       # Depth: 1
    songs {             # Depth: 2
      album {           # Depth: 3
        songs {         # Depth: 4
          album {id: N} # Depth: N
        }
      }
    }
  }
}
```

Excessive Amount Request Example:
```javascript
query {
  author(id: "abc") {
    posts(first: 99999999) {
      title
    }
  }
}
```

Batching Attack Example:
```javascript
[
  {
    query: < query 0 >,
    variables: < variables for query 0 >,
  },
  {
    query: < query 1 >,
    variables: < variables for query 1 >,
  },
  {
    query: < query n >
    variables: < variables for query n >,
  }
]
```

Summary:  
Secure GraphQL APIs through comprehensive input validation, query limiting, proper access controls, batching attack prevention, secure configuration management, and robust authentication mechanisms while preventing common attack vectors like injection, DoS, and unauthorized data access.