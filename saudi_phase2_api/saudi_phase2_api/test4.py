import hashlib
import base64
from lxml import etree
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from datetime import datetime
import xml.etree.ElementTree as ET
import json
import xml.dom.minidom as minidom
import requests

def invoiceHash():
    import xml.etree.ElementTree as ET

    # Load the XML file
    xml_file_path = "/opt/oxy/frappe-bench/apps/saudi_phase2_api/saudi_phase2_api/saudi_phase2_api/test1.xml"
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Define namespaces
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
    element = root.find(xpath_expression, namespaces=namespaces)

    # Extract the text from the element
    if element is not None:
        result = element.text
        print("Text at the specified path:", result)
        return result
    else:
        print("Element not found at the specified path.")


xml_file = "/opt/oxy/frappe-bench/apps/saudi_phase2_api/saudi_phase2_api/saudi_phase2_api/test1.xml"
tree = etree.parse(xml_file)

# Remove specified tags using XPath
tags_to_remove = ["//ext:UBLExtensions", "//cbc:Signature", "//cbc:AdditionalDocumentReference[cbc:ID='QR']"]
for tag in tags_to_remove:
    for element in tree.xpath(tag, namespaces={"ext": "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2",
                                                "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" , 
                                                'cac':"urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"}):
        element.getparent().remove(element)
        print('-------------')

# Canonicalize the Invoice
xml_str = etree.tostring(tree.getroot(), method="c14n", exclusive=False, with_comments=False)

# Hash the new invoice body using SHA-256
invoice_hash = hashlib.sha256(xml_str).digest()

# Encode the hashed invoice using base64
encoded_invoice_hash = base64.b64encode(invoice_hash).decode()

print("Encoded Invoice Hash:", encoded_invoice_hash)


# encoded_xml = xml_file.encode('utf-8')
# # Hash the encoded XML
# invoice_hash = hashlib.sha256(encoded_xml).digest()
# # invoice_hash = hashlib.sha256(xml_str).digest()
# print("invoice_hash:  " ,  invoice_hash)
# encoded_invoice_hash = base64.b64encode(invoice_hash).decode() 
# print("encoded_invoice_hash:  " ,  encoded_invoice_hash)

# decoded_invoice_hash = base64.b64decode(encoded_invoice_hash)  # for testing only
# print("decoded_invoice_hash:  " ,  decoded_invoice_hash)  # for testing only



with open("/opt/oxy/frappe-bench/sites/helloprikey.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())
    # Sign the invoice hash
    signature = private_key.sign(invoice_hash, ec.ECDSA(hashes.SHA256()))
    # Encode the signature using base64
    encoded_signature = base64.b64encode(signature).decode()
    print("Encoded Signature:", encoded_signature)



decoded_binary_security_token = ""
with open('/opt/oxy/frappe-bench/sites/response_from_send_csr.json' , 'r') as json_file : 
        data = json.load(json_file)
        decoded_binary_security_token = base64.b64decode(data['binarySecurityToken'])
# Load your certificate

encoded_certificate_hash = ""
certificate_hash = hashlib.sha256(decoded_binary_security_token).digest()
# Encode the hashed certificate using base64
encoded_certificate_hash = base64.b64encode(certificate_hash).decode()
print("Encoded Certificate Hash:", encoded_certificate_hash)
# Load the original invoice XML


original_invoice_xml = etree.parse('/opt/oxy/frappe-bench/apps/saudi_phase2_api/saudi_phase2_api/saudi_phase2_api/test1.xml')
root = original_invoice_xml.getroot()
# Define the namespaces for convenience

namespaces = {
'ext': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2',
'sig': 'urn:oasis:names:specification:ubl:schema:xsd:CommonSignatureComponents-2',
'sac':"urn:oasis:names:specification:ubl:schema:xsd:SignatureAggregateComponents-2", 
'xades': 'http://uri.etsi.org/01903/v1.3.2#',
'ds': 'http://www.w3.org/2000/09/xmldsig#'
}

# Define XPath expressions
ubl_extensions_xpath = "//*[local-name()='Invoice']//*[local-name()='UBLExtensions']"
qr_xpath = "//*[local-name()='AdditionalDocumentReference'][cbc:ID[normalize-space(text()) = 'QR']]"
signature_xpath = "//*[local-name()='Invoice']//*[local-name()='Signature']"

# Modify the XPath expression to be relative to the root element
xpath_dv = (
    "ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:Object/xades:QualifyingProperties/xades:SignedProperties/xades:SignedSignatureProperties/xades:SigningCertificate/xades:Cert/xades:CertDigest/ds:DigestValue"
)

xpath_signTime = (
    "ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:Object/xades:QualifyingProperties/xades:SignedProperties/xades:SignedSignatureProperties/xades:SigningTime"
)

xpath_issuerName = (
    "ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:Object/xades:QualifyingProperties/xades:SignedProperties/xades:SignedSignatureProperties/xades:SigningCertificate/xades:Cert/xades:IssuerSerial/ds:X509IssuerName"
)

xpath_serialNum = (
    "ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:Object/xades:QualifyingProperties/xades:SignedProperties//xades:SignedSignatureProperties/xades:SigningCertificate/xades:Cert/xades:IssuerSerial/ds:X509SerialNumber"
)

# Find the element using the modified relative XPath
element_dv = root.find(xpath_dv, namespaces)
element_st = root.find(xpath_signTime , namespaces)
element_in = root.find(xpath_issuerName , namespaces)
element_sn = root.find(xpath_serialNum , namespaces)

element_dv.text = (encoded_certificate_hash)
element_st.text =  str(datetime.utcnow().isoformat())
element_in.text =  'CN=TSZEINVOICE-SubCA-1, DC=extgazt, DC=gov, DC=local'
element_sn.text =  '7012364670'

with open("/opt/oxy/frappe-bench/sites/after.xml", 'wb') as file:
    original_invoice_xml.write(
        file,
        encoding='utf-8',
        xml_declaration=True,
    )


# step 5 -- generate signed properties hash 
xml_from_step_4 = etree.parse('/opt/oxy/frappe-bench/sites/after.xml')
root2 = original_invoice_xml.getroot()
xpath_signedProp = (
    "ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:Object/xades:QualifyingProperties/xades:SignedProperties")
signed_prop_tag = root2.find(xpath_signedProp , namespaces)
# serialize the tag to string without spaces 
signed_properties_xml = ET.tostring(signed_prop_tag , encoding='utf-8').decode().replace(" ", "")
# print(signed_properties_xml)
# Hash the serialized SignedProperties using SHA-256
signed_properties_hash = hashlib.sha256(signed_properties_xml.encode()).digest()
signed_properties_hex = signed_properties_hash.hex()
signed_properties_base64 = base64.b64encode(bytes.fromhex(signed_properties_hex)).decode()
# Encode the hash using HEX-to-Base64 Encoder
# signed_properties_base64 = base64.b64encode(signed_properties_hash).decode()
print("signed properties",signed_properties_base64)
  

# Step 6: Populate The UBL Extensions Output

# Load the updated invoice XML (from Step 4)
updated_invoice_xml = etree.parse('/opt/oxy/frappe-bench/sites/after.xml')
root3 = updated_invoice_xml.getroot()

xpath_signvalue = (
    "ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:SignatureValue"
)
xpath_x509certi = (
    "ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:KeyInfo/ds:X509Data/ds:X509Certificate"
)
xpath_digvalue = (
    "ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:SignedInfo/ds:Reference[@URI='#xadesSignedProperties']/ds:DigestValue"
)
xpath_digvalue2 = ( "ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:SignedInfo/ds:Reference[@Id='invoiceSignedData']/ds:DigestValue")

# Use XPath to find the UBL Extensions element
signValue6 = root3.find(xpath_signvalue , namespaces)
x509Certificate6 = root3.find(xpath_x509certi , namespaces)
digestvalue6 = root3.find(xpath_digvalue , namespaces)
digestvalue6_2 = root3.find(xpath_digvalue2 , namespaces)

signValue6.text = (encoded_signature)
x509Certificate6.text = (decoded_binary_security_token)
digestvalue6.text = (signed_properties_base64)
digestvalue6_2.text = (encoded_invoice_hash)


with open("/opt/oxy/frappe-bench/sites/final.xml", 'wb') as file:
    updated_invoice_xml.write(file,encoding='utf-8',xml_declaration=True,)
signedXmlFilePath = "/opt/oxy/frappe-bench/sites/final.xml"
with open(signedXmlFilePath, "r") as file:
    xml = file.read().lstrip()
    base64_encoded = base64.b64encode(xml.encode("utf-8"))
    base64_decoded = base64_encoded.decode("utf-8") 
url = "https://gw-fatoora.zatca.gov.sa/e-invoicing/developer-portal/compliance/invoices"
payload = json.dumps({
"invoiceHash": invoiceHash(),
"uuid": "3cf5ee18-ee25-44ea-a444-2c37ba7f28be",
"invoice": base64_decoded
})
headers = { 
    'accept': 'application/json',
    'Accept-Language': 'en',
    'Accept-Version': 'V2',
    'Authorization': "Basic VFVsSlJERnFRME5CTTNsblFYZEpRa0ZuU1ZSaWQwRkJaVFJUYUhOMmVXNDNNREo1VUhkQlFrRkJRamRvUkVGTFFtZG5jV2hyYWs5UVVWRkVRV3BDYWsxU1ZYZEZkMWxMUTFwSmJXbGFVSGxNUjFGQ1IxSlpSbUpIT1dwWlYzZDRSWHBCVWtKbmIwcHJhV0ZLYXk5SmMxcEJSVnBHWjA1dVlqTlplRVo2UVZaQ1oyOUthMmxoU21zdlNYTmFRVVZhUm1ka2JHVklVbTVaV0hBd1RWSjNkMGRuV1VSV1VWRkVSWGhPVlZVeGNFWlRWVFZYVkRCc1JGSlRNVlJrVjBwRVVWTXdlRTFDTkZoRVZFbDVUVVJaZUUxNlJURk5la1V3VG14dldFUlVTVEJOUkZsNFRXcEZNVTE2UlRCT2JHOTNVMVJGVEUxQmEwZEJNVlZGUW1oTlExVXdSWGhFYWtGTlFtZE9Wa0pCYjFSQ1YwWnVZVmQ0YkUxU1dYZEdRVmxFVmxGUlRFVjNNVzlaV0d4b1NVaHNhRm95YUhSaU0xWjVUVkpKZDBWQldVUldVVkZFUlhkcmVFMXFZM1ZOUXpSM1RHcEZkMVpxUVZGQ1oyTnhhR3RxVDFCUlNVSkNaMVZ5WjFGUlFVTm5Ua05CUVZSVVFVczViSEpVVm10dk9YSnJjVFphV1dOak9VaEVVbHBRTkdJNVV6UjZRVFJMYlRkWldFb3JjMjVVVm1oTWEzcFZNRWh6YlZOWU9WVnVPR3BFYUZKVVQwaEVTMkZtZERoREwzVjFWVms1TXpSMmRVMU9ielJKUTB0cVEwTkJhVmwzWjFselIwRXhWV1JGVVZOQ1ozcERRbWRMVWl0TlNIZDRTRlJCWWtKblRsWkNRVkZOUmtSRmRHRkhSalZaV0hkNVRGUkplazVJZDNwTVZFVjRUV3BOZWsxU09IZElVVmxMUTFwSmJXbGFVSGxNUjFGQ1FWRjNVRTE2VFhoTlZGbDVUMFJaTlU1RVFYZE5SRUY2VFZFd2QwTjNXVVJXVVZGTlJFRlJlRTFVUVhkTlVrVjNSSGRaUkZaUlVXRkVRV2hoV1ZoU2FsbFRRWGhOYWtWWlRVSlpSMEV4VlVWRWQzZFFVbTA1ZGxwRFFrTmtXRTU2WVZjMWJHTXpUWHBOUWpCSFFURlZaRVJuVVZkQ1FsTm5iVWxYUkRaaVVHWmlZa3RyYlZSM1QwcFNXSFpKWWtnNVNHcEJaa0puVGxaSVUwMUZSMFJCVjJkQ1VqSlpTWG8zUW5GRGMxb3hZekZ1WXl0aGNrdGpjbTFVVnpGTWVrSlBRbWRPVmtoU09FVlNla0pHVFVWUFoxRmhRUzlvYWpGdlpFaFNkMDlwT0haa1NFNHdXVE5LYzB4dWNHaGtSMDVvVEcxa2RtUnBOWHBaVXpsRVdsaEtNRkpYTlhsaU1uaHpUREZTVkZkclZrcFViRnBRVTFWT1JreFdUakZaYTA1Q1RGUkZkVmt6U25OTlNVZDBRbWRuY2tKblJVWkNVV05DUVZGVFFtOUVRMEp1VkVKMVFtZG5ja0puUlVaQ1VXTjNRVmxhYVdGSVVqQmpSRzkyVEROU2VtUkhUbmxpUXpVMldWaFNhbGxUTlc1aU0xbDFZekpGZGxFeVZubGtSVloxWTIwNWMySkRPVlZWTVhCR1lWYzFNbUl5YkdwYVZrNUVVVlJGZFZwWWFEQmFNa1kyWkVNMWJtSXpXWFZpUnpscVdWZDRabFpHVG1GU1ZXeFBWbXM1U2xFd1ZYUlZNMVpwVVRCRmRFMVRaM2hMVXpWcVkyNVJkMHQzV1VsTGQxbENRbEZWU0UxQlIwZElNbWd3WkVoQk5reDVPVEJqTTFKcVkyMTNkV1Z0UmpCWk1rVjFXakk1TWt4dVRtaE1NamxxWXpOQmQwUm5XVVJXVWpCUVFWRklMMEpCVVVSQloyVkJUVUl3UjBFeFZXUktVVkZYVFVKUlIwTkRjMGRCVVZWR1FuZE5RMEpuWjNKQ1owVkdRbEZqUkVGNlFXNUNaMnR5UW1kRlJVRlpTVE5HVVc5RlIycEJXVTFCYjBkRFEzTkhRVkZWUmtKM1RVTk5RVzlIUTBOelIwRlJWVVpDZDAxRVRVRnZSME5EY1VkVFRUUTVRa0ZOUTBFd1owRk5SVlZEU1ZGRVQxQXdaakJFY21oblpVUlVjbFpNZEVwMU9HeFhhelJJU25SbFkyWTFabVpsVWt4blpVUTRZMlZWWjBsblpFSkNUakl4U1RNM2FYTk5PVlZ0VTFGbE9IaFNjRWh1ZDA5NFNXYzNkMDR6V1RKMlZIQnpVR2hhU1QwPTpFcGo2OUdoOFRNTXpZZktsdEx2MW9tWktyaWUwc1A2TEF2YW1iUUZIVGd3PQ==",
    'Content-Type': 'application/json'}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)




