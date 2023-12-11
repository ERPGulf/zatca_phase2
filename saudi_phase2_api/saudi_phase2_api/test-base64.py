import binascii

# Convert the ASCII string to a byte string
data = b"\xe7\xfbzRk\x15\xb3\xec\xf9\x80.(\xf65\x04@\xea\xdd\xc3\x0c\xd7\x91'g\xc8\x82\xdb/\xd5\xd2?\x9c"

# Convert the byte string to hex
hex_data = binascii.hexlify(data)

# Convert the hex string back to byte string
byte_data = binascii.unhexlify(hex_data)

# Print the byte data
print(byte_data)