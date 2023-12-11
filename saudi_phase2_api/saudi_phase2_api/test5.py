import xml.etree.ElementTree as ET
from lxml import etree

xml_file = "/opt/oxy/frappe-bench/sites/finalzatcaxml.xml"
tree = etree.parse(xml_file)
tags_to_remove = ["//ext:UBLExtensions", "//cbc:Signature", "//cbc:AdditionalDocumentReference[cbc:ID='QR']"]
for tag in tags_to_remove:
    for element in tree.xpath(tag, namespaces={"ext": "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2",
                                                "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" , 
                                                'cac':"urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"}):
        element.getparent().remove(element)
        print('-------------')
# Canonicalize the Invoice
xml_str = etree.tostring(tree.getroot(), method="c14n", exclusive=False, with_comments=False)
print("xml str is",xml_str)