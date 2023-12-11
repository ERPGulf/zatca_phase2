import xml.etree.ElementTree as ET

# Your XML data
xml_data = """<?xml version='1.0' encoding='UTF-8'?>
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2">
    <ext:UBLExtensions>
        <ext:UBLExtension>
            <ext:ExtensionURI>urn:oasis:names:specification:ubl:dsig:enveloped:xades</ext:ExtensionURI>
            <ext:ExtensionContent>
                <sig:UBLDocumentSignatures xmlns:sig="urn:oasis:names:specification:ubl:schema:xsd:CommonSignatureComponents-2" xmlns:sac="urn:oasis:names:specification:ubl:schema:xsd:SignatureAggregateComponents-2" xmlns:sbc="urn:oasis:names:specification:ubl:schema:xsd:SignatureBasicComponents-2">
                    <sac:SignatureInformation>
                        <cbc:ID>urn:oasis:names:specification:ubl:signature:1</cbc:ID>
                        <sbc:ReferencedSignatureID>urn:oasis:names:specification:ubl:signature:Invoice</sbc:ReferencedSignatureID>

                    <ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" Id="signature">
  <ds:SignedInfo>
    <ds:CanonicalizationMethod Algorithm="http://www.w3.org/2006/12/xml-c14n11"/>
    <ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#ecdsa-sha256"/>
    <ds:Reference Id="invoiceSignedData" URI=""><ds:Transforms><ds:Transform Algorithm="http://www.w3.org/TR/1999/REC-xpath-19991116"><ds:XPath>not(//ancestor-or-self::ext:UBLExtensions)</ds:XPath></ds:Transform><ds:Transform Algorithm="http://www.w3.org/TR/1999/REC-xpath-19991116"><ds:XPath>not(//ancestor-or-self::cac:Signature)</ds:XPath></ds:Transform><ds:Transform Algorithm="http://www.w3.org/TR/1999/REC-xpath-19991116"><ds:XPath>not(//ancestor-or-self::cac:AdditionalDocumentReference[cbc:ID='QR'])</ds:XPath></ds:Transform><ds:Transform Algorithm="http://www.w3.org/2006/12/xml-c14n11"/></ds:Transforms>
      <ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
      <ds:DigestValue>+jzBMOVEUC2kFNYIMBQwxBK7SvVDbDarasCaUOacFrA=</ds:DigestValue>
    </ds:Reference>
    <ds:Reference Type="http://www.w3.org/2000/09/xmldsig#SignatureProperties" URI="#xadesSignedProperties">
      <ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
      <ds:DigestValue>jdZBeuev8vvL02rE1PzEeRr4ZMO4x/PrQPOO9JmOwGk=</ds:DigestValue>
    </ds:Reference>
  </ds:SignedInfo>
  <ds:SignatureValue>MEYCIQClpRGJBXE5b51fZVZ1EJ7Bfepal0y6lBBKLKSCuDdlHwIhAM/zAJLbkOQfkEuzCE7qvMv85D7b71l4AXeifS08lJeu</ds:SignatureValue>
  <ds:KeyInfo>
    <ds:X509Data>
      <ds:X509Certificate>MIICLzCCAdSgAwIBAgIGAYw+reHPMAoGCCqGSM49BAMCMBUxEzARBgNVBAMMCmVJbnZvaWNpbmcwHhcNMjMxMjA2MTAzMDI3WhcNMjgxMjA1MjEwMDAwWjBjMQswCQYDVQQGEwJTQTEYMBYGA1UECwwPQXhpcyBJbnNwZWN0aW9uMSgwJgYDVQQKDB9BeGlzIEluc3BlY3Rpb24gQ29udHJhY3RpbmcgSlNDMRAwDgYDVQQDDAdlcnBuZXh0MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAESpezV60yCUOtPQhh6fgGwE4xwaDn9Nqrk2e56WZtO2YZ/h4f2XztJ2GMr1xwuRVOQbgccNn/ZZVavAEjVvjiyaOBxDCBwTAMBgNVHRMBAf8EAjAAMIGwBgNVHREEgagwgaWkgaIwgZ8xKzApBgNVBAQMIjEtQXhpc0luc3BlY3Rpb258Mi0xM3wzLTcwMTIzNjQ2NzAxHzAdBgoJkiaJk/IsZAEBDA8zMDA5NzA4MDYxMDAwMDMxDTALBgNVBAwMBDExMDAxEjAQBgNVBBoMCUFsLUtob2JhcjEsMCoGA1UEDwwjSW5kdXN0cmlhbCBzZXJ2aWNlcyBhbmQgY29udHJhY3RpbmcwCgYIKoZIzj0EAwIDSQAwRgIhAKW1L3FIiC5lxEHQWKnM0THEQ4wcHhNW8ZigmOHgNfO4AiEAxq73WCh3YqYaPuKZQI6IBDHhmqEVJ4osNG9XnoWJBVw=</ds:X509Certificate>
    </ds:X509Data>
  </ds:KeyInfo>
  <ds:Object>
    <xades:QualifyingProperties xmlns:xades="http://uri.etsi.org/01903/v1.3.2#" Target="signature">
    <xades:SignedProperties Id="xadesSignedProperties">
        <xades:SignedSignatureProperties>
            <xades:SigningTime>2023-12-06T10:42:10.521783</xades:SigningTime>
            <xades:SigningCertificate>
                <xades:Cert>
                    <xades:CertDigest>
                        <ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
                        <ds:DigestValue>yhqru+1e7JJiSJ7wAGx1Yjoun6BeKQ5CzOs8nPn7D0I=</ds:DigestValue>
                    </xades:CertDigest>
                    <xades:IssuerSerial>
                        <ds:X509IssuerName>CN=TSZEINVOICE-SubCA-1, DC=extgazt, DC=gov, DC=local</ds:X509IssuerName>
                        <ds:X509SerialNumber>7012364670</ds:X509SerialNumber>
                    </xades:IssuerSerial>
                </xades:Cert>
            </xades:SigningCertificate>
        </xades:SignedSignatureProperties>
    </xades:SignedProperties>
</xades:QualifyingProperties>
</ds:Object>
</ds:Signature></sac:SignatureInformation>
                </sig:UBLDocumentSignatures>
            </ext:ExtensionContent>
        </ext:UBLExtension>
    </ext:UBLExtensions>

    <cbc:ProfileID>reporting:1.0</cbc:ProfileID>
    <cbc:ID>100</cbc:ID>
    <cbc:UUID>3cf5ee18-ee25-44ea-a444-2c37ba7f28be</cbc:UUID>
    <cbc:IssueDate>2021-04-25</cbc:IssueDate>
    <cbc:IssueTime>15:30:00</cbc:IssueTime>
    <cbc:InvoiceTypeCode name="0100000">388</cbc:InvoiceTypeCode>
    <cbc:DocumentCurrencyCode>SAR</cbc:DocumentCurrencyCode>
    <cbc:TaxCurrencyCode>SAR</cbc:TaxCurrencyCode>
    <cbc:LineCountNumeric>2</cbc:LineCountNumeric>
    <cac:AdditionalDocumentReference>
        <cbc:ID>ICV</cbc:ID>
        <cbc:UUID>46531</cbc:UUID>
    </cac:AdditionalDocumentReference>
    <cac:AdditionalDocumentReference>
        <cbc:ID>PIH</cbc:ID>
        <cac:Attachment>
            <cbc:EmbeddedDocumentBinaryObject mimeCode="text/plain">NWZl......NTdlOQ==</cbc:EmbeddedDocumentBinaryObject>
        </cac:Attachment>
    </cac:AdditionalDocumentReference>


    <cac:AdditionalDocumentReference>
        <cbc:ID>QR</cbc:ID>
        <cac:Attachment>
            <cbc:EmbeddedDocumentBinaryObject mimeCode="text/plain">AQxGaXJveiBBc2hyYWYCCjEyMzQ1Njc4OTEDEzIwMjEtMTEtMTcgMDg6MzA6MDAEBjEwMC4wMAUFMTUuMDAGLGdwVjV1REpTQVIzaC9vUnowUzNYZGdOeUlFRTlBSGNBRHR2bFA1T3NlL3M9</cbc:EmbeddedDocumentBinaryObject>
        </cac:Attachment>
    </cac:AdditionalDocumentReference>
    <cac:Signature>
        <cbc:ID>urn:oasis:names:specification:ubl:signature:Invoice</cbc:ID>
        <cbc:SignatureMethod>urn:oasis:names:specification:ubl:dsig:enveloped:xades</cbc:SignatureMethod>
    </cac:Signature>
    <cac:AccountingSupplierParty>
        <cac:Party>
            <cac:PartyIdentification>
                <cbc:ID schemeID="MLS">123457890</cbc:ID>
            </cac:PartyIdentification>
            <cac:PostalAddress>
                <cbc:StreetName>King Abdulaziz Road</cbc:StreetName>
                <cbc:BuildingNumber>9999</cbc:BuildingNumber>
                <cbc:PlotIdentification>9999</cbc:PlotIdentification>
                <cbc:CitySubdivisionName>Al Amal</cbc:CitySubdivisionName>
                <cbc:CityName>Riyadh</cbc:CityName>
                <cbc:PostalZone>12643</cbc:PostalZone>
                <cbc:CountrySubentity>Riyadh Region</cbc:CountrySubentity>
                <cac:Country>
                    <cbc:IdentificationCode>SA</cbc:IdentificationCode>
                </cac:Country>
            </cac:PostalAddress>
            <cac:PartyTaxScheme>
                <cbc:CompanyID>300099999900003</cbc:CompanyID>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:PartyTaxScheme>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName>Example Co. LTD</cbc:RegistrationName>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:AccountingSupplierParty>
    <cac:AccountingCustomerParty>
        <cac:Party>
            <cac:PartyIdentification>
                <cbc:ID schemeID="SAG">123C12345678</cbc:ID>
            </cac:PartyIdentification>
            <cac:PostalAddress>
                <cbc:StreetName>King Abdullah Road</cbc:StreetName>
                <cbc:BuildingNumber>9999</cbc:BuildingNumber>
                <cbc:PlotIdentification>9999</cbc:PlotIdentification>
                <cbc:CitySubdivisionName>Al Mursalat</cbc:CitySubdivisionName>
                <cbc:CityName>Riyadh</cbc:CityName>
                <cbc:PostalZone>11564</cbc:PostalZone>
                <cbc:CountrySubentity>Riyadh Region</cbc:CountrySubentity>
                <cac:Country>
                    <cbc:IdentificationCode>SA</cbc:IdentificationCode>
                </cac:Country>
            </cac:PostalAddress>
            <cac:PartyTaxScheme>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:PartyTaxScheme>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName>EXAMPLE MARKETS</cbc:RegistrationName>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:AccountingCustomerParty>
    <cac:Delivery>
        <cbc:ActualDeliveryDate>2022-04-25</cbc:ActualDeliveryDate>
    </cac:Delivery>
    <cac:PaymentMeans>
        <cbc:PaymentMeansCode>42</cbc:PaymentMeansCode>
    </cac:PaymentMeans>
    <cac:TaxTotal>
        <cbc:TaxAmount currencyID="SAR">135.00</cbc:TaxAmount>
        <cac:TaxSubtotal>
            <cbc:TaxableAmount currencyID="SAR">900.00</cbc:TaxableAmount>
            <cbc:TaxAmount currencyID="SAR">135.00</cbc:TaxAmount>
            <cac:TaxCategory>
                <cbc:ID>S</cbc:ID>
                <cbc:Percent>15</cbc:Percent>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:TaxCategory>
        </cac:TaxSubtotal>
    </cac:TaxTotal>
    <cac:TaxTotal>
        <cbc:TaxAmount currencyID="SAR">135.00</cbc:TaxAmount>
    </cac:TaxTotal>
    <cac:LegalMonetaryTotal>
        <cbc:LineExtensionAmount currencyID="SAR">900.00</cbc:LineExtensionAmount>
        <cbc:TaxExclusiveAmount currencyID="SAR">900.00</cbc:TaxExclusiveAmount>
        <cbc:TaxInclusiveAmount currencyID="SAR">1035.00</cbc:TaxInclusiveAmount>
        <cbc:AllowanceTotalAmount currencyID="SAR">0.00</cbc:AllowanceTotalAmount>
        <cbc:PayableAmount currencyID="SAR">1035.00</cbc:PayableAmount>
    </cac:LegalMonetaryTotal>
    <cac:InvoiceLine>
        <cbc:ID>1</cbc:ID>
        <cbc:InvoicedQuantity unitCode="PCE">1</cbc:InvoicedQuantity>
        <cbc:LineExtensionAmount currencyID="SAR">200.00</cbc:LineExtensionAmount>
        <cac:TaxTotal>
            <cbc:TaxAmount currencyID="SAR">30.00</cbc:TaxAmount>
            <cbc:RoundingAmount currencyID="SAR">230.00</cbc:RoundingAmount>
        </cac:TaxTotal>
        <cac:Item>
            <cbc:Name>Item A</cbc:Name>
            <cac:ClassifiedTaxCategory>
                <cbc:ID>S</cbc:ID>
                <cbc:Percent>15</cbc:Percent>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:ClassifiedTaxCategory>
        </cac:Item>
        <cac:Price>
            <cbc:PriceAmount currencyID="SAR">200.00</cbc:PriceAmount>
        </cac:Price>
    </cac:InvoiceLine>
    <cac:InvoiceLine>
        <cbc:ID>2</cbc:ID>
        <cbc:InvoicedQuantity unitCode="PCE">2</cbc:InvoicedQuantity>
        <cbc:LineExtensionAmount currencyID="SAR">700.00</cbc:LineExtensionAmount>
        <cac:TaxTotal>
            <cbc:TaxAmount currencyID="SAR">105.00</cbc:TaxAmount>
            <cbc:RoundingAmount currencyID="SAR">805.00</cbc:RoundingAmount>
        </cac:TaxTotal>
        <cac:Item>
            <cbc:Name>Item B</cbc:Name>
            <cac:ClassifiedTaxCategory>
                <cbc:ID>S</cbc:ID>
                <cbc:Percent>15</cbc:Percent>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:ClassifiedTaxCategory>
        </cac:Item>
        <cac:Price>
            <cbc:PriceAmount currencyID="SAR">350.00</cbc:PriceAmount>
        </cac:Price>
    </cac:InvoiceLine>
</Invoice>"""

# Parse the XML data
root = ET.fromstring(xml_data)

# Define the namespace mapping
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
else:
    print("Element not found at the specified path.")
