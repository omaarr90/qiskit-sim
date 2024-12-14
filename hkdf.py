import hashlib
import hmac
import math

# Convert bits to bytes
def bits_to_bytes(bit_array):
    byte_array = bytearray()
    for i in range(0, len(bit_array), 8):
        byte = 0
        for bit in bit_array[i:i+8]:
            byte = (byte << 1) | bit
        byte_array.append(byte)
    return bytes(byte_array)

# HKDF Extract
def hkdf_extract(salt, ikm, hash_function=hashlib.sha256):
    if salt is None:
        salt = b'\x00' * hash_function().digest_size
    return hmac.new(salt, ikm, hash_function).digest()

def hkdf_expand(prk, info, length, hash_function=hashlib.sha256):
    hash_len = hash_function().digest_size
    num_blocks = math.ceil(length / hash_len)
    okm = b''
    output_block = b''

    # Ensure `info` is bytes
    if not isinstance(info, bytes):
        info = bytes(info)  # Convert list to bytes if needed

    for i in range(1, num_blocks + 1):
        output_block = hmac.new(prk, output_block + info + bytes([i]), hash_function).digest()
        okm += output_block

    return okm[:length]

def convert(bits, output_length_in_bytes):
    if len(bits) >= output_length_in_bytes * 8:
        return bits

    ikm = bits_to_bytes(bits)   
    
    # Derive the key using HKDF
    salt = None
    prk = hkdf_extract(salt, ikm)
    okm = hkdf_expand(prk, bits, output_length_in_bytes)

    # Output the derived key as a 48-bit binary string
    output_key = int.from_bytes(okm, 'big')
    # print(f"48-bit derived key: {bin(output_key)[2:].zfill(48)}")
    return okm