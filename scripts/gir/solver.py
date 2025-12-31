def xor_decrypt(ciphertext, key=7): 
    """Decrypts a string using a single byte XOR key.""" 
    plaintext = "" 
    for char in ciphertext: 
        # XOR the ASCII value of the character with the key 
        decrypted_char = chr(ord(char) ^ key) 
        plaintext += decrypted_char 
    return plaintext 
# Data from BASIC source 
enc_pass = "D13URKBT" 
enc_flag = "DSA|auhts*wkfi=dhjwubtthut+dhhkfis+hnkz" 

# Execution 
password = xor_decrypt(enc_pass) 
flag = xor_decrypt(enc_flag) 

print(f"[*] Password Found: {password}") 
print(f"[*] Flag Found: {flag}")
