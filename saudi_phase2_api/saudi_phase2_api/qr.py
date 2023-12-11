import xml.etree.ElementTree as ET
from xml.dom import minidom
import base64
import sys
import re
import xml.etree.ElementTree as ET

def get_signed_xml_invoice_for_clearance(signedXmlFilePath):
    try:
        signedXmlFilePath="/opt/oxy/frappe-bench/sites/final_xml_after_sign.xml"
        xmlSigned = ET.parse(signedXmlFilePath)
        # Print the entire XML document for debugging
        ET.dump(xmlSigned.getroot())

        # Define the namespaces used in the XPath expression
        namespaces = {
            'ext': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2',
            'sig': 'urn:oasis:names:specification:ubl:schema:xsd:CommonSignatureComponents-2',
            'sac': 'urn:oasis:names:specification:ubl:schema:xsd:SignatureAggregateComponents-2',
            'ds': 'http://www.w3.org/2000/09/xmldsig#',
        }
        # Define the XPath expression
        xpath_expression = (
            ".//ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/"
            "sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/"
            "ds:SignedInfo/ds:Reference[1]/ds:DigestValue"
        )        
        # Find the element using XPath
        element = xmlSigned.find(xpath_expression, namespaces=namespaces)
        # Extract the text from the element
        if element is not None:
            sbDigestValue = element.text
            print("Text at the specified path:", sbDigestValue)
        else:
            print("Element not found at the specified path.")
            sys.exit()
        return sbDigestValue, xmlSigned, signedXmlFilePath
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit()

def generate_tlv_xml():
    sellerName = "Firoz Ashraf"
    vatNumber = "1234567891"
    timeStamp = "2021-11-17 08:30:00"
    invoiceTotal = "100.00"
    vatTotal = "15.00"
    tag = 1
    tlv_data = []
    tlv_data.append(bytes([tag]))
    tlv_data.append(sellerName.encode('utf-8'))
    tag += 1
    tlv_data.append(bytes([tag]))
    tlv_data.append(vatNumber.encode('utf-8'))
    tag += 1
    tlv_data.append(bytes([tag]))
    tlv_data.append(timeStamp.encode('utf-8'))
    tag += 1
    tlv_data.append(bytes([tag]))
    tlv_data.append(invoiceTotal.encode('utf-8'))
    tag += 1
    tlv_data.append(bytes([tag]))
    tlv_data.append(vatTotal.encode('utf-8'))
    sbDigestValue, xmlSigned, signedXmlFilePath = get_signed_xml_invoice_for_clearance("/opt/oxy/frappe-bench/sites/final_xml_after_sign.xml")
    tag = 6
    tlv_data.append(bytes([tag]))
    tlv_data.append(len(sbDigestValue).to_bytes(1, byteorder='big'))
    tlv_data.append(sbDigestValue.encode('utf-8'))
    tlv_encoded = base64.b64encode(b''.join(tlv_data)).decode('utf-8')
    print (tlv_encoded)
    return tlv_encoded

# Function to recursively search for the target element
def find_and_update():
    signedXmlFilePath="/opt/oxy/frappe-bench/sites/final_xml_after_sign.xml"
    tree = ET.parse(signedXmlFilePath)
    root = tree.getroot()

    # Define namespaces
    namespace = {
        'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
        'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
    }

    # Find the element to be replaced
    target_element = root.find(".//cac:AdditionalDocumentReference[cbc:ID='QR']/cac:Attachment/cbc:EmbeddedDocumentBinaryObject", namespaces=namespace)
    # Replace the text content with your TLV data variable
    tlv_data_variable = generate_tlv_xml()
    target_element.text = tlv_data_variable

    # Write the modified XML content back to the file
    tree.write("signedXML_withQR1234.xml", encoding="utf-8", xml_declaration=True)

    print("XML file has been successfully modified.")
generate_tlv_xml()
find_and_update()

