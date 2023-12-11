import hashlib

def calculate_sha256(xml_string):
    # Encode the XML string to bytes
    xml_bytes = xml_string.encode('utf-8')

    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the XML bytes
    sha256_hash.update(xml_bytes)

    # Get the hexadecimal representation of the hash
    hash_result = sha256_hash.hexdigest()

    return hash_result

# Example XML string
example_xml = """
<root>
    <element1>Value1</element1>
    <element2>Value2</element2>
</root>
"""
# Calculate SHA-256 hash
sha256_result = calculate_sha256(example_xml)

# Print the result
print("SHA-256 Hash:", sha256_result)