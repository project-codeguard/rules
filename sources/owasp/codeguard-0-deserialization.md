---
description: Deserialization Security Best Practices
languages:
- c
- java
- javascript
- php
- python
- xml
- yaml
alwaysApply: false
version: 0.1.0
severity: medium
---

## Avoid Unsafe Deserialization of Untrusted Data

Deserialization of untrusted input can lead to critical vulnerabilities such as remote code execution, denial of service, and privilege escalation. This rule ensures developers follow best practices to safely handle serialization and deserialization operations.

Requirements:

- Always treat incoming serialized data from untrusted sources as hostile.
- Validate input size, structure, and content before deserialization.
- Prefer standardized, safe data formats like JSON or XML without type metadata over native serialization formats.
- For XML: disable DTDs and external entities to prevent XXE attacks.
- Avoid using unsafe native serialization APIs on untrusted input, such as:
  - PHP: avoid `unserialize()`, use `json_decode()`/`json_encode()` instead.
  - Python: avoid `pickle.loads`, `yaml.load` (use `safe_load`), and `jsonpickle` on untrusted data.
  - Java: override `ObjectInputStream#resolveClass()` to allowlist classes; mark sensitive fields `transient`; avoid polymorphic deserialization unless strictly allowlisted.
  - .NET: avoid `BinaryFormatter`; use `DataContractSerializer` or `XmlSerializer`; set `TypeNameHandling = None` in JSON.Net; never trust deserialized types blindly.
- Sign serialized data and verify signatures to ensure integrity before deserialization.
- Configure serialization libraries securely:
  - Jackson: `mapper.enableDefaultTyping(ObjectMapper.DefaultTyping.NON_FINAL)` is dangerous
  - fastjson: Enable safemode, disable autotype
  - XStream: Use allowlists with `XStream.allowTypes()`
  - SnakeYAML: Use `yaml.safe_load()` instead of `yaml.load()`
  - Keep dependencies updated to fixed versions.
- Reject or safely handle polymorphic or complex objects deserialization from untrusted sources.
- Use hardened deserialization agents/tools (e.g., SerialKiller, hardened ObjectInputStream subclasses, JVM agents).
- Log deserialization attempts and monitor for suspicious activity.
- Regularly scan code and dependencies for unsafe deserialization patterns using static and dynamic analysis tools.

Security Impact:

Deserialization attacks are a frequently exploited vector leading to severe security impacts. Following these practices prevents attackers from injecting malicious objects or payloads that the application may execute.

Examples:

Avoid:
- PHP: calling `unserialize($data)` on external input.
- Java: deserializing classes without strict allowlisting or type validation.
- Python: loading YAML with `yaml.load()` on untrusted data.
- .NET: using `BinaryFormatter.Deserialize()` on untrusted input.
- XML: processing XML with DTDs enabled or external entity resolution.

Recommended:
- PHP: use `json_decode()` and validate JSON schema.
- Java: Override `resolveClass()` to allowlist safe classes:
  ```java
  @Override
  protected Class<?> resolveClass(ObjectStreamClass desc) throws IOException, ClassNotFoundException {
      if (!allowedClasses.contains(desc.getName())) {
          throw new InvalidClassException("Unauthorized class", desc.getName());
      }
      return super.resolveClass(desc);
  }
  ```
- Python: Use safe YAML loading:
  ```python
  import yaml
  data = yaml.safe_load(input)  # Safe
  # Never: yaml.load(input)     # Dangerous
  ```
- .NET: Use DataContractSerializer with type control:
  ```csharp
  // Safe approach
  var serializer = new DataContractSerializer(typeof(SafeType));
  var obj = serializer.ReadObject(stream);
  
  // JSON.NET safety
  JsonConvert.DeserializeObject<SafeType>(json, new JsonSerializerSettings {
      TypeNameHandling = TypeNameHandling.None
  });
  ```
- XML: Configure parsers safely:
  ```java
  // Java: Disable DTDs and external entities
  factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
  factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
  ```
  ```csharp
  // .NET: Disable DTD processing
  XmlReaderSettings settings = new XmlReaderSettings();
  settings.DtdProcessing = DtdProcessing.Prohibit;
  ```

Monitoring Requirements:
- Log all deserialization attempts with data size and type information
- Alert on deserialization failures or unexpected data patterns
- Monitor for known malicious payloads (e.g., `AC ED 00 05`, `rO0`, `AAEAAAD`)
- Track deserialization performance to detect "billion laughs" attacks