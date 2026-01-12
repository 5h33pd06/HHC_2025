from PIL import Image

def decrypt_shadow(image_path):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size
    
    # 1. Extract the Encrypted Bytes from the Blue Channel
    enc_data = bytearray()
    for i in range(width * height):
        x = i % width
        y = i // width
        # The script put the byte in the Blue channel (R, G, B) -> index 2
        byte = pixels[x, y][2]
        enc_data.append(byte)

    # 2. Decrypt (CBC Mode Reverse: P[i] = C[i] ^ C[i-1])
    BLOCK_SIZE = 6
    plaintext = bytearray()
    
    print(f"[*] Total bytes extracted: {len(enc_data)}")
    
    for i in range(BLOCK_SIZE, len(enc_data)):
        p_byte = enc_data[i] ^ enc_data[i - BLOCK_SIZE]
        plaintext.append(p_byte)

    # 3. Print the result
    try:
        print("-" * 30)
        print("RECOVERED SHADOW FILE (First 6 bytes missing):")
        print("-" * 30)
        print(plaintext.decode('utf-8', errors='ignore'))
        print("-" * 30)
    except Exception as e:
        print(f"Error decoding: {e}")
        print("Raw bytes:")
        print(plaintext)

if __name__ == "__main__":
    try:
        decrypt_shadow("shadow.png")
    except FileNotFoundError:
        print("Error: shadow.png not found. Please place the exfiltrated PNG in this directory.")
