

import xml.etree.ElementTree as ET

# Parse the XML file into an ElementTree
tree = ET.parse('/opt/oxy/frappe-bench/apps/saudi_phase2_api/saudi_phase2_api/saudi_phase2_api/dum.xml')

# Get the root element
root = tree.getroot()

# Declare the namespace for 'cbc'
ET.register_namespace('cbc', 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2')

# Find the element with the attribute "currencyID"
element_to_update = root.find('.//cbc:InvoiceAmount[@currencyID]', namespaces={'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'})

# Update the value of the "currencyID" attribute
element_to_update.attrib['currencyID'] = '83432423'

# Convert the XML tree to a string after the update
xml_string_after_currency_update = ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')

# Print the XML string after updating the currencyID
print(xml_string_after_currency_update)






