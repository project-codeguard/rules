---
description: XML External Entity Prevention
languages:
- c
- java
- matlab
- php
- python
- swift
- xml
alwaysApply: false
version: 0.1.0
severity: medium
---

## XML External Entity Prevention

Prevent XXE attacks by disabling DTDs and external entities in XML parsers. Safest approach: disable DTDs completely.

### General Principle

```java
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
```

Disabling DTDs protects against XXE and Billion Laughs attacks. If DTDs cannot be disabled, disable external entities using parser-specific methods.

### Java

Java parsers have XXE enabled by default.

DocumentBuilderFactory/SAXParserFactory/DOM4J:

```java
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
String FEATURE = null;
try {
    // PRIMARY defense - disallow DTDs completely
    FEATURE = "http://apache.org/xml/features/disallow-doctype-decl";
    dbf.setFeature(FEATURE, true);
    dbf.setXIncludeAware(false);
} catch (ParserConfigurationException e) {
    logger.info("ParserConfigurationException was thrown. The feature '" + FEATURE
    + "' is not supported by your XML processor.");
}
```

If DTDs cannot be completely disabled:

```java
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
String[] featuresToDisable = {
    "http://xml.org/sax/features/external-general-entities",
    "http://xml.org/sax/features/external-parameter-entities",
    "http://apache.org/xml/features/nonvalidating/load-external-dtd"
};

for (String feature : featuresToDisable) {
    try {    
        dbf.setFeature(feature, false); 
    } catch (ParserConfigurationException e) {
        logger.info("ParserConfigurationException was thrown. The feature '" + feature
        + "' is probably not supported by your XML processor.");
    }
}
dbf.setXIncludeAware(false);
dbf.setExpandEntityReferences(false);
dbf.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);
```

XMLInputFactory (StAX):
```java
xmlInputFactory.setProperty(XMLInputFactory.SUPPORT_DTD, false);
// Or if DTDs needed:
xmlInputFactory.setProperty(XMLConstants.ACCESS_EXTERNAL_DTD, "");
xmlInputFactory.setProperty("javax.xml.stream.isSupportingExternalEntities", false);
```

TransformerFactory:
```java
TransformerFactory tf = TransformerFactory.newInstance();
tf.setAttribute(XMLConstants.ACCESS_EXTERNAL_DTD, "");
tf.setAttribute(XMLConstants.ACCESS_EXTERNAL_STYLESHEET, "");
```

XMLReader:
```java
XMLReader reader = XMLReaderFactory.createXMLReader();
reader.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
reader.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
reader.setFeature("http://xml.org/sax/features/external-general-entities", false);
reader.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
```

SAXBuilder:
```java
SAXBuilder builder = new SAXBuilder();
builder.setFeature("http://apache.org/xml/features/disallow-doctype-decl",true);
Document doc = builder.build(new File(fileName));
```

No-op EntityResolver:
```java
public final class NoOpEntityResolver implements EntityResolver {
    public InputSource resolveEntity(String publicId, String systemId) {
        return new InputSource(new StringReader(""));
    }
}
xmlReader.setEntityResolver(new NoOpEntityResolver());
documentBuilder.setEntityResolver(new NoOpEntityResolver());
```

Never use java.beans.XMLDecoder on untrusted content - it can execute arbitrary code.

### .NET

XmlReader (.NET 4.5.2+ safe by default):
```csharp
XmlReaderSettings settings = new XmlReaderSettings();
settings.DtdProcessing = DtdProcessing.Prohibit;
settings.XmlResolver = null;
XmlReader reader = XmlReader.Create(stream, settings);
```

XmlTextReader (prior to .NET 4.0):
```csharp
XmlTextReader reader = new XmlTextReader(stream);
reader.ProhibitDtd = true;  
```

XmlTextReader (.NET 4.0 - 4.5.2):
```csharp
XmlTextReader reader = new XmlTextReader(stream);
reader.DtdProcessing = DtdProcessing.Prohibit;  
```

XmlDocument (prior to 4.5.2):
```csharp
XmlDocument xmlDoc = new XmlDocument();
xmlDoc.XmlResolver = null;
xmlDoc.LoadXml(xml);
```

XPathNavigator (prior to 4.5.2):
```csharp
XmlReader reader = XmlReader.Create("example.xml");
XPathDocument doc = new XPathDocument(reader);
XPathNavigator nav = doc.CreateNavigator();
string xml = nav.InnerXml.ToString();
```

### C/C++

libxml2: Avoid XML_PARSE_NOENT and XML_PARSE_DTDLOAD options.

libxerces-c:
```cpp
XercesDOMParser *parser = new XercesDOMParser;
parser->setCreateEntityReferenceNodes(true);
parser->setDisableDefaultEntityResolution(true);

SAXParser* parser = new SAXParser;
parser->setDisableDefaultEntityResolution(true);

SAX2XMLReader* reader = XMLReaderFactory::createXMLReader();
parser->setFeature(XMLUni::fgXercesDisableDefaultEntityResolution, true);
```

### PHP

PHP 8.0+ prevents XXE by default. Earlier versions:
```php
libxml_set_external_entity_loader(null);
```

### Python

```python
from defusedxml import ElementTree as ET
tree = ET.parse('filename.xml')

# Or with lxml:
from lxml import etree
parser = etree.XMLParser(resolve_entities=False, no_network=True)
tree = etree.parse('filename.xml', parser)
```

### iOS/macOS

```swift
let options: NSXMLNodeOptions = .documentTidyXML
let xmlDoc = try NSXMLDocument(data: data, options: options.union(.nodeLoadExternalEntitiesNever))
```

### ColdFusion

Adobe ColdFusion:
```
<cfset parseroptions = structnew()>
<cfset parseroptions.ALLOWEXTERNALENTITIES = false>
<cfscript>
a = XmlParse("xml.xml", false, parseroptions);
</cfscript>
```

Lucee (Application.cfc):
```
this.xmlFeatures = {
     externalGeneralEntities: false,
     secure: true,
     disallowDoctypeDecl: true
};
```

### Additional Measures

- Update XML libraries regularly
- Validate XML input before parsing
- Use static analysis tools for XXE detection
- Test with XXE payloads in safe environments

### When DTDs Required

If DTDs absolutely necessary:
- Use custom EntityResolver with restricted entities
- Implement strict entity allowlisting
- Preprocess XML to remove dangerous DOCTYPE declarations