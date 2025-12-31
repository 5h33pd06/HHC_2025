import binascii
import random

# Global constant from Source 924
MOUNTAIN_WIDTH = 1000

class Mountain:
    def __init__(self, name, height, encoded_flag):
        self.name = name
        self.height = height
        self.encoded_flag = encoded_flag

    def get_treasure_keys(self):
        # Logic reversed from Mountain.GetTreasureLocations (Source 426)
        
        # 1. Seed based on name (Source 437-442)
        random.seed(binascii.crc32(self.name.encode('utf-8')))
        
        prev_height = self.height
        prev_horiz = 0
        treasure_keys = []

        # Loop 5 times (Source 447)
        for _ in range(5):
            # Calculate Elevation Delta (Source 450-453)
            e_delta = random.randint(200, 800)
            
            # Calculate Horizontal Delta (Source 454-462)
            # int((0 - e_delta) / 4) and int(e_delta / 4)
            lower_bound = int((0 - e_delta) / 4)
            upper_bound = int(e_delta / 4)
            h_delta = random.randint(lower_bound, upper_bound)
            
            # Update locations (Source 466-468)
            # Note: The code updates prev_height AFTER calculating the location for the dict
            # In the disassembly, locations[prev_height - e_delta] = prev_horiz + h_delta
            
            current_height = prev_height - e_delta
            current_horiz = prev_horiz + h_delta
            
            # In main (Source 808), the value appended is:
            # collided_row[0] * mountain_width + collided_row_offset
            # collided_row[0] is elevation. collided_row_offset is horizontal index.
            # GetObstacles (Source 413) places treasures at `treasure_h % mountain_width`
            
            final_val = (current_height * MOUNTAIN_WIDTH) + (current_horiz % MOUNTAIN_WIDTH)
            treasure_keys.append(final_val)

            # Update for next iteration
            prev_height = current_height
            prev_horiz = current_horiz

        return treasure_keys

def decrypt_flag(mountain):
    keys = mountain.get_treasure_keys()
    
    # Logic from SetFlag (Source 638-644)
    product = 0
    for val in keys:
        product = (product << 8) ^ val
    
    # Decrypt (Source 645-660)
    random.seed(product)
    decoded = []
    
    for byte_val in mountain.encoded_flag:
        r = random.randint(0, 255)
        decoded.append(chr(byte_val ^ r))
        
    return "".join(decoded)

# Data extracted from Source 1040 - 1059 (Mountain definitions)
mountains_data = [
    ("Mount Snow", 3586, b'\x90\x00\x1d\xbc\x17b\xed6S"\xb0<Y\xd6\xce\x169\xae\xe9|\xe2Gs\xb7\xfdy\xcf5\x98'),
    ("Aspen", 11211, b'U\xd7%x\xbfvj!\xfe\x9d\xb9\xc2\xd1k\x02y\x17\x9dK\x98\xf1\x92\x0f!\xf1\\\xa0\x1b\x0f'),
    ("Whistler", 7156, b'\x1cN\x13\x1a\x97\xd4\xb2!\xf9\xf6\xd4#\xee\xebh\xecs.\x08M!hr9?\xde\x0c\x86\x02'),
    ("Mount Baker", 10781, b'\xac\xf9#\xf4T\xf1%h\xbe3FI+h\r\x01V\xee\xc2C\x13\xf3\x97ef\xac\xe3z\x96'),
    ("Mount Norquay", 6998, b'\x0c\x1c\xad!\xc6,\xec0\x0b+"\x9f@.\xc8\x13\xadb\x86\xea{\xfeS\xe0S\x85\x90\x03q'),
    ("Mount Erciyes", 12848, b'n\xad\xb4l^I\xdb\xe1\xd0\x7f\x92\x92\x96\x1bq\xca`PvWg\x85\xb21^\x93F\x1a\xee'),
    ("Dragonmount", 16282, b'Z\xf9\xdf\x7f_\x02\xd8\x89\x12\xd2\x11p\xb6\x96\x19\x05x))v\xc3\xecv\xf4\xe2\\\x9a\xbe\xb5')
]

print("Attempting to decrypt flags for all mountains...\n")

for name, height, enc_flag in mountains_data:
    mnt = Mountain(name, height, enc_flag)
    try:
        flag = decrypt_flag(mnt)
        print(f"Mountain: {name}")
        print(f"Result:   {flag}")
        print("-" * 40)
    except Exception as e:
        print(f"Mountain: {name} - Failed: {e}")
