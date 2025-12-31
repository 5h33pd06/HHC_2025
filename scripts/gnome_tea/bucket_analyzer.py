import requests
import json
import urllib.parse
import os

# -------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------
BUCKET_NAME = "holidayhack2025.firebasestorage.app"
# Using the Admin UID as the token since it worked for listing
AUTH_TOKEN = "3loaihgxP0VwCTKmkHHFLe6FZ4m2"
DOWNLOAD_DIR = "downloaded_gnome_files"
# -------------------------------------------------------

def download_all_files():
    print(f"[*] Starting mass download from bucket: {BUCKET_NAME}")
    
    # Create download directory if it doesn't exist
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    # 1. List all objects in the bucket
    # Documentation: https://firebase.google.com/docs/storage/web/list-files
    list_url = f"https://firebasestorage.googleapis.com/v0/b/{BUCKET_NAME}/o"
    
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }
    
    # We request a large page size to get everything at once
    params = {"maxResults": 1000}

    try:
        print("[*] Fetching file list...")
        response = requests.get(list_url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"[-] Failed to list files! Status: {response.status_code}")
            print(f"    Response: {response.text}")
            return

        data = response.json()
        items = data.get('items', [])
        
        print(f"[+] Found {len(items)} files. Beginning download...\n")

        # 2. Iterate and Download
        for item in items:
            file_path = item.get('name') # e.g., "gnome-documents/license.jpg"
            
            # Create local subdirectory structure if needed
            local_path = os.path.join(DOWNLOAD_DIR, file_path.replace("/", "_"))
            
            # Construct the download URL
            # IMPORTANT: We must URL-encode the path (replace '/' with '%2F') for the API
            safe_name = urllib.parse.quote(file_path, safe='')
            download_url = f"https://firebasestorage.googleapis.com/v0/b/{BUCKET_NAME}/o/{safe_name}?alt=media"
            
            print(f"    ⬇️  Downloading: {file_path} ...", end=" ")
            
            file_resp = requests.get(download_url, headers=headers)
            
            if file_resp.status_code == 200:
                with open(local_path, "wb") as f:
                    f.write(file_resp.content)
                print("✅ Saved.")
                
            else:
                print(f"❌ Failed ({file_resp.status_code})")

        print(f"\n[*] Download complete. Check the '{DOWNLOAD_DIR}' folder.")

    except Exception as e:
        print(f"[-] Script Crash: {e}")

if __name__ == "__main__":
    download_all_files()
