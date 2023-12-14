import frappe
# frappe.init(site="husna.erpgulf.com")
# frappe.connect()
import requests    
import pyqrcode
import os
import hashlib
import base64
from lxml import etree
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from datetime import datetime
import xml.etree.ElementTree as ET
import json
from OpenSSL import crypto
from lxml import etree
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography import x509
from subprocess import call
from subprocess import check_output
def create_Csr():
    print("hello")
    cmd = "openssl ecparam -name secp256k1 -genkey -noout -out prikey.pem"
    decrypted1 = call(cmd, shell=True)
    output = check_output(cmd, shell=True)
    print(output.decode('utf-8'))
    
    cmd1="openssl ec -in prikey.pem -pubout -conv_form compressed -out pubkey.pem"
    decrypted2 = call(cmd1, shell=True) 
    print(decrypted2)
    cmd2="openssl req -new -sha256 -key privatekey3.pem -extensions v3_req -config /opt/oxy/frappe-bench/apps/saudi_phase2_api/saudi_phase2_api/saudi_phase2_api/csrconfig.txt -out taxpayer3.csr" 
    decrypted3 = call(cmd2, shell=True)  
    cmd3="openssl base64 -in taxpayer3.csr -out taxpayerCSRbase64Encoded3.txt" 
    decrypted4 = call(cmd3, shell=True) 
    with open(r'taxpayerCSRbase64Encoded3.txt', 'r') as file:
        data = file.read()
        data = data.replace("\n","")
        data = data.replace("\r","")
    with open(r'taxpayerCSRbase64Encoded3.txt', 'w') as file:
        file.write(data)
        print("done")
    print(data)
    return data
# create_Csr()

def signxml():
    original_invoice_xml = etree.parse('/opt/oxy/frappe-bench/apps/saudi_phase2_api/saudi_phase2_api/saudi_phase2_api/new_test.xml')
    root = original_invoice_xml.getroot()
    # Define the namespaces for convenience
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

    # element_dv.text = "125633"

    element_st.text =  str(datetime.utcnow().isoformat())

    element_in.text =  'CN=TSZEINVOICE-SubCA-1, DC=extgazt, DC=gov, DC=local'

    element_sn.text =  '7012364670'

signxml()

