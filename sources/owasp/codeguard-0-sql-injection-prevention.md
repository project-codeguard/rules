---
description: SQL Injection Prevention Guidelines
languages:
- c
- go
- java
- javascript
- perl
- php
- python
- ruby
- sql
- typescript
alwaysApply: false
version: 0.1.0
severity: medium
---

## SQL Injection Prevention Guidelines

Essential practices for preventing SQL injection attacks by using secure database query construction methods instead of string concatenation.

### Understanding SQL Injection

SQL injection occurs when applications use dynamic database queries that concatenate user input directly into SQL strings. Attackers can exploit this to execute malicious SQL code. To prevent SQL injection, developers must either stop writing dynamic queries with string concatenation or prevent malicious SQL input from being included in executed queries.

### Primary Defense Options

#### Option 1: Prepared Statements (Parameterized Queries) - Preferred

Use prepared statements with variable binding to separate SQL code from data. The database will always distinguish between code and data, preventing attackers from changing query intent.

Safe Java example:
```java
// This should REALLY be validated too
String custname = request.getParameter("customerName");
// Perform input validation to detect attacks
String query = "SELECT account_balance FROM user_data WHERE user_name = ? ";
PreparedStatement pstmt = connection.prepareStatement( query );
pstmt.setString( 1, custname);
ResultSet results = pstmt.executeQuery( );
```

Safe C# .NET example:
```csharp
String query = "SELECT account_balance FROM user_data WHERE user_name = ?";
try {
  OleDbCommand command = new OleDbCommand(query, connection);
  command.Parameters.Add(new OleDbParameter("customerName", CustomerName Name.Text));
  OleDbDataReader reader = command.ExecuteReader();
  // …
} catch (OleDbException se) {
  // error handling
}
```

Safe HQL example:
```java
// This is an unsafe HQL statement
Query unsafeHQLQuery = session.createQuery("from Inventory where productID='"+userSuppliedParameter+"'");
// Here is a safe version of the same query using named parameters
Query safeHQLQuery = session.createQuery("from Inventory where productID=:productid");
safeHQLQuery.setParameter("productid", userSuppliedParameter);
```

#### Option 2: Stored Procedures (When Implemented Safely)

Use stored procedures only if inputs are parameterized and no dynamic SQL generation occurs within them.

Safe Java stored procedure example:
```java
// This should REALLY be validated
String custname = request.getParameter("customerName");
try {
  CallableStatement cs = connection.prepareCall("{call sp_getAccountBalance(?)}");
  cs.setString(1, custname);
  ResultSet results = cs.executeQuery();
  // … result set handling
} catch (SQLException se) {
  // … logging and error handling
}
```

Safe VB .NET stored procedure example:
```vbnet
 Try
   Dim command As SqlCommand = new SqlCommand("sp_getAccountBalance", connection)
   command.CommandType = CommandType.StoredProcedure
   command.Parameters.Add(new SqlParameter("@CustomerName", CustomerName.Text))
   Dim reader As SqlDataReader = command.ExecuteReader()
   '...
 Catch se As SqlException
   'error handling
 End Try
```

#### Option 3: Allow-list Input Validation

For SQL elements that cannot use bind variables (table names, column names, sort indicators), use strict allow-listing.

Safe table name validation:
```text
String tableName;
switch(PARAM):
  case "Value1": tableName = "fooTable";
                 break;
  case "Value2": tableName = "barTable";
                 break;
  ...
  default      : throw new InputValidationException("unexpected value provided"
                                                  + " for table name");
```

Safe dynamic query for sort order:
```java
public String someMethod(boolean sortOrder) {
 String SQLquery = "some SQL ... order by Salary " + (sortOrder ? "ASC" : "DESC");`
 ...
```

#### Option 4: Escaping (Strongly Discouraged)

Escaping user input is database-specific, error-prone, and cannot guarantee prevention of all SQL injections. Use parameterized queries instead.

### Additional Defenses

#### Least Privilege

Minimize privileges for all database accounts:
- Grant only necessary access rights (read vs. write)
- Avoid DBA or admin access for application accounts
- Use separate database users for different applications
- Consider using views to limit data access further

#### Input Validation

Use input validation as a secondary defense to detect unauthorized input before SQL execution. Validated data is not necessarily safe for string concatenation - always use parameterized queries.

### Key Principles

- Define all SQL code first, then pass parameters separately
- Never concatenate user input directly into SQL strings
- Treat user input as data, never as executable SQL code
- Use least privilege database accounts
- Implement input validation as defense in depth, not primary protection