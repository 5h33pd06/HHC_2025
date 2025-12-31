import requests
import json
import os

# -------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------
PROJECT_ID = "holidayhack2025"
API_KEY = "AIzaSyDvBE5-77eZO8T18EiJ_MwGAYo5j2bqhbk"
TARGET_COLLECTIONS = ["gnomes", "tea", "dms"]
# -------------------------------------------------------

def unwrap_value(value):
    """
    Recursively unwraps Firestore-style JSON (e.g. {'stringValue': 'x'})
    into standard Python types.
    """
    if not isinstance(value, dict):
        return value
    
    # Handle specific Firestore value types
    if 'stringValue' in value: return value['stringValue']
    if 'integerValue' in value: return int(value['integerValue'])
    if 'doubleValue' in value: return float(value['doubleValue'])
    if 'booleanValue' in value: return value['booleanValue']
    if 'timestampValue' in value: return value['timestampValue']
    if 'bytesValue' in value: return value['bytesValue']
    if 'referenceValue' in value: return value['referenceValue']
    
    # Recursive types (Maps and Arrays)
    if 'mapValue' in value:
        # mapValue contains a 'fields' dict
        return unwrap_fields(value['mapValue'].get('fields', {}))
    if 'arrayValue' in value:
        # arrayValue contains a 'values' list
        return [unwrap_value(v) for v in value['arrayValue'].get('values', [])]
    
    return value

def unwrap_fields(fields):
    """Converts a Firestore 'fields' dictionary into a clean Python dict."""
    clean_dict = {}
    for key, val in fields.items():
        clean_dict[key] = unwrap_value(val)
    return clean_dict

def dump_collection(collection_name):
    print(f"[*] Fetching collection: '{collection_name}'...")
    
    # Firestore REST API endpoint
    # pageSize=1000 is usually enough for CTFs, but you can implement paging if needed
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/{collection_name}?key={API_KEY}&pageSize=1000"
    
    try:
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"[-] Failed to fetch {collection_name}: {response.status_code} - {response.text}")
            return

        data = response.json()
        documents = data.get('documents', [])
        
        print(f"[+] Retrieved {len(documents)} documents.")
        
        # Process and clean the data
        cleaned_data = []
        for doc in documents:
            # Get the clean dictionary
            doc_data = unwrap_fields(doc.get('fields', {}))
            # Add metadata ID for reference
            doc_data['_id'] = doc['name'].split('/')[-1]
            cleaned_data.append(doc_data)
            
        # Save to file
        filename = f"{collection_name}_dump.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, indent=2)
            
        print(f"[+] Saved cleanly to '{filename}'\n")

    except Exception as e:
        print(f"[-] Exception dumping {collection_name}: {e}")

if __name__ == "__main__":
    print(f"--- 🎅 Starting Holiday Hack Data Dump 🎅 ---\n")
    
    for col in TARGET_COLLECTIONS:
        dump_collection(col)
        
    print("--- Dump Complete ---")
    print("You can now grep/search the .json files for 'password', 'login', or 'credential'.")
