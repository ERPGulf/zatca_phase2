import xml.etree.ElementTree as ET

# Create the root element
root = ET.Element('Invoice', xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2")
# Create a "cac" element
cac_element = ET.SubElement(root, 'cac:Party')
cac_name = ET.SubElement(cac_element, 'cac:PartyName')
cac_name_value = ET.SubElement(cac_name, 'cbc:Name')
cac_name_value.text = 'ABC Corp'

# Create a "cbc" element
cbc_element = ET.SubElement(root, 'cbc:InvoiceAmount')
cbc_element.text = '1000.00'
cbc_element.attrib['currencyID'] = 'USD'

# Insert a new "cbc:Discount" element
discount_element = ET.SubElement(root, 'cbc:Discount')
discount_element.text = '50.00'
discount_element.attrib['currencyID'] = 'USD'

# Convert the XML tree to a string
xml_string = ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')

# Print the XML string
print(xml_string)
print('--------------editint it after---------------')

# Update the value of the "cbc:InvoiceAmount" element
cbc_element.text = '300000.94'

# Convert the XML tree to a string after the update
xml_string_after_update = ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')

# Print the XML string after the update
print(xml_string_after_update)