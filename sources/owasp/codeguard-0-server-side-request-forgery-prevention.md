---
description: Server-Side Request Forgery Prevention
languages:
- c
- go
- java
- javascript
- php
- python
- ruby
- typescript
alwaysApply: false
---

## Server-Side Request Forgery Prevention

Prevent SSRF attacks that abuse applications to interact with internal/external networks by validating and restricting outbound requests.

### SSRF Attack Context

SSRF exploits occur when applications:
- Process user-provided URLs for external resources (avatars, webhooks)
- Make internal requests using user-controlled data
- Handle URL redirections without proper validation

SSRF is not limited to HTTP - attackers can exploit FTP, SMB, SMTP protocols and schemes like `file://`, `phar://`, `gopher://`, `data://`, `dict://`.

### Case 1: Allowlist Approach (Known Trusted Destinations)

When applications communicate only with identified trusted applications, use strict allowlisting.

#### Application Layer Protection

Always disable HTTP redirects in web clients to prevent bypass attempts.

#### String Validation
Use regex for simple formats, libraries for complex validation:

```java
//Regex validation for a data having a simple format
if(Pattern.matches("[a-zA-Z0-9\\s\\-]{1,50}", userInput)){
    //Continue the processing because the input data is valid
}else{
    //Stop the processing and reject the request
}
```

#### IP Address Validation
Use battle-tested libraries to validate IP format and prevent encoding bypasses:

- Java: `InetAddressValidator.isValid()` from Apache Commons Validator
- .NET: `IPAddress.TryParse()` from SDK
- JavaScript: `ip-address` library  
- Ruby: `IPAddr` class from SDK

Create allowlist of all trusted application IPs (IPv4 and IPv6). Use output value from validation library for strict string comparison against allowlist.

#### Domain Name Validation
Use libraries that validate format without DNS resolution:

- Java: `DomainValidator.isValid()` from Apache Commons Validator
- .NET: `Uri.CheckHostName()` from SDK
- JavaScript: `is-valid-domain` library
- Python: `validators.domain` module
- Ruby: Use regex `^(((?!-))(xn--|_{1,1})?[a-z0-9-]{0,61}[a-z0-9]{1,1}\.)*(xn--)?([a-z0-9][a-z0-9\-]{0,60}|[a-z0-9-]{1,30}\.[a-z]{2,})$`

Monitor allowlisted domains for DNS pinning attacks - alert when domains resolve to local/internal IP addresses.

#### URL Handling
Do not accept complete URLs from users. URLs are difficult to validate and parsers can be exploited. Accept only validated IP addresses or domain names.

#### Network Layer Protection
- Use firewalls to restrict application network access to only required destinations
- Implement network segregation to block illegitimate calls at network level
- Define legitimate flows and block all others

### Case 2: Dynamic External Destinations (Block-list Approach)

When applications must access arbitrary external resources (webhooks), use block-list validation.

#### Validation Flow
1. Validate input format using libraries from Case 1
2. For IP addresses: Verify it's public (not private, localhost, or link-local)
3. For domains: 
   - Verify it's external using internal DNS resolver that only resolves internal names
   - Resolve domain to IPs and validate all returned addresses are public
4. Restrict protocols to HTTP/HTTPS only via allowlist
5. Require legitimate request proof via secure token

#### Secure Token Requirements
- Target application generates random 20-character alphanumeric token
- Token passed as POST parameter with name using only `[a-z]{1,10}` characters
- Endpoint accepts only HTTP POST requests
- Build requests using only validated information

#### Example Python Monitoring Script
Monitor allowlisted domains for DNS pinning:

```python
# Dependencies: pip install ipaddress dnspython
import ipaddress
import dns.resolver

# Configure the allowlist to check
DOMAINS_ALLOWLIST = ["owasp.org", "labslinux"]

# Configure the DNS resolver to use for all DNS queries
DNS_RESOLVER = dns.resolver.Resolver()
DNS_RESOLVER.nameservers = ["1.1.1.1"]

def verify_dns_records(domain, records, type):
    """
    Verify if one of the DNS records resolve to a non public IP address.
    Return a boolean indicating if any error has been detected.
    """
    error_detected = False
    if records is not None:
        for record in records:
            value = record.to_text().strip()
            try:
                ip = ipaddress.ip_address(value)
                # See https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Address.is_global
                if not ip.is_global:
                    print("[!] DNS record type '%s' for domain name '%s' resolve to a non public IP address '%s'!" % (type, domain, value))
                    error_detected = True
            except ValueError:
                error_detected = True
                print("[!] '%s' is not valid IP address!" % value)
    return error_detected

def check():
    """
    Perform the check of the allowlist of domains.
    Return a boolean indicating if any error has been detected.
    """
    error_detected = False
    for domain in DOMAINS_ALLOWLIST:
        # Get the IPs of the current domain
        # See https://en.wikipedia.org/wiki/List_of_DNS_record_types
        try:
            # A = IPv4 address record
            ip_v4_records = DNS_RESOLVER.query(domain, "A")
        except Exception as e:
            ip_v4_records = None
            print("[i] Cannot get A record for domain '%s': %s\n" % (domain,e))
        try:
            # AAAA = IPv6 address record
            ip_v6_records = DNS_RESOLVER.query(domain, "AAAA")
        except Exception as e:
            ip_v6_records = None
            print("[i] Cannot get AAAA record for domain '%s': %s\n" % (domain,e))
        # Verify the IPs obtained
        if verify_dns_records(domain, ip_v4_records, "A") or verify_dns_records(domain, ip_v6_records, "AAAA"):
            error_detected = True
    return error_detected

if __name__== "__main__":
    if check():
        exit(1)
    else:
        exit(0)
```

### Cloud-Specific Protections

#### AWS IMDSv2
In cloud environments, SSRF targets metadata services to steal credentials. Migrate to IMDSv2 and disable IMDSv1 for additional protection against SSRF accessing AWS Instance Metadata Service.

### Essential Implementation Guidelines

1. Never accept raw URLs from users - validate only IP addresses or domain names
2. Use established libraries for IP/domain validation to prevent encoding bypasses  
3. Implement strict allowlists with case-sensitive exact matching for trusted destinations
4. Disable HTTP redirects in all outbound HTTP clients
5. For dynamic destinations, block private/internal IP ranges and validate DNS resolution
6. Restrict protocols to HTTP/HTTPS only
7. Require secure tokens for request legitimacy verification
8. Apply network-layer restrictions via firewalls and segmentation
9. Monitor allowlisted domains for DNS pinning attacks
10. Use cloud-specific protections like AWS IMDSv2