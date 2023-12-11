import chilkat2
import sys

with open(f"/opt/oxy/frappe-bench/sites/myxml.xml", 'r') as file:
        invoice_xml = file.read()
def add_Static_Valueto_Xml(invoice_xml):   
                    sbXml = chilkat2.StringBuilder()
                    sbXml.Append(invoice_xml)
                    if sbXml.Length == 0:
                        print("Failed to load XML content to be signed.")
                        sys.exit()
                    gen = chilkat2.XmlDSigGen()
                    gen.SigLocation = "Invoice|ext:UBLExtensions|ext:UBLExtension|ext:ExtensionContent|sig:UBLDocumentSignatures|sac:SignatureInformation"
                    gen.SigLocationMod = 0
                    gen.SigId = "signature"
                    gen.SigNamespacePrefix = "ds"
                    gen.SigNamespaceUri = "http://www.w3.org/2000/09/xmldsig#"
                    gen.SignedInfoCanonAlg = "C14N_11"
                    gen.SignedInfoDigestMethod = "sha256"
                    object1 = chilkat2.Xml()
                    object1.Tag = "xades:QualifyingProperties"
                    object1.AddAttribute("xmlns:xades","http://uri.etsi.org/01903/v1.3.2#")
                    object1.AddAttribute("Target","signature")
                    object1.UpdateAttrAt("xades:SignedProperties",True,"Id","xadesSignedProperties")
                    object1.UpdateChildContent("xades:SignedProperties|xades:SignedSignatureProperties|xades:SigningTime","TO BE GENERATED BY CHILKAT")
                    object1.UpdateAttrAt("xades:SignedProperties|xades:SignedSignatureProperties|xades:SigningCertificate|xades:Cert|xades:CertDigest|ds:DigestMethod",True,"Algorithm","http://www.w3.org/2001/04/xmlenc#sha256")
                    object1.UpdateChildContent("xades:SignedProperties|xades:SignedSignatureProperties|xades:SigningCertificate|xades:Cert|xades:CertDigest|ds:DigestValue","TO BE GENERATED BY CHILKAT")
                    object1.UpdateChildContent("xades:SignedProperties|xades:SignedSignatureProperties|xades:SigningCertificate|xades:Cert|xades:IssuerSerial|ds:X509IssuerName","TO BE GENERATED BY CHILKAT")
                    object1.UpdateChildContent("xades:SignedProperties|xades:SignedSignatureProperties|xades:SigningCertificate|xades:Cert|xades:IssuerSerial|ds:X509SerialNumber","TO BE GENERATED BY CHILKAT")
                    gen.AddObject("",object1.GetXml(),"","")
                    xml1 = chilkat2.Xml()
                    xml1.Tag = "ds:Transforms"
                    xml1.UpdateAttrAt("ds:Transform",True,"Algorithm","http://www.w3.org/TR/1999/REC-xpath-19991116")
                    xml1.UpdateChildContent("ds:Transform|ds:XPath","not(//ancestor-or-self::ext:UBLExtensions)")
                    xml1.UpdateAttrAt("ds:Transform[1]",True,"Algorithm","http://www.w3.org/TR/1999/REC-xpath-19991116")
                    xml1.UpdateChildContent("ds:Transform[1]|ds:XPath","not(//ancestor-or-self::cac:Signature)")
                    xml1.UpdateAttrAt("ds:Transform[2]",True,"Algorithm","http://www.w3.org/TR/1999/REC-xpath-19991116")
                    xml1.UpdateChildContent("ds:Transform[2]|ds:XPath","not(//ancestor-or-self::cac:AdditionalDocumentReference[cbc:ID='QR'])")
                    xml1.UpdateAttrAt("ds:Transform[3]",True,"Algorithm","http://www.w3.org/2006/12/xml-c14n11")
                    gen.AddSameDocRef2("","sha256",xml1,"")
                    gen.SetRefIdAttr("","invoiceSignedData")
                    gen.AddObjectRef("xadesSignedProperties","sha256","","","http://www.w3.org/2000/09/xmldsig#SignatureProperties")
                    print(sbXml)
                    print(gen)
                    return gen,sbXml  

def load_certificate(gen,sbXml): 
                    certFromPfx = chilkat2.Cert()
                    success = certFromPfx.LoadPfxFile("/opt/oxy/frappe-bench/sites/mycert.pfx","Friday2000@T")
                    if (success != True):
                        print(certFromPfx.LastErrorText)
                        sys.exit()
                    success = gen.SetX509Cert(certFromPfx,True)
                    if (success != True):
                        print(gen.LastErrorText)
                        sys.exit()
                    gen.KeyInfoType = "X509Data"
                    gen.X509Type = "Certificate"
                    gen.Behaviors = "IndentedSignature,TransformSignatureXPath,ZATCA"
                    success = gen.CreateXmlDSigSb(sbXml)
                    if (success != True):
                        print(gen.LastErrorText)
                        sys.exit()
                    return sbXml

def create_File_SignedXML(sbXml):
                    success = sbXml.WriteFile("signedXml.xml","utf-8",False)
                    return sbXml


gen,sbXml =add_Static_Valueto_Xml(invoice_xml)
# sbXml=load_certificate(gen,sbXml)
# sbXml=create_File_SignedXML(sbXml)