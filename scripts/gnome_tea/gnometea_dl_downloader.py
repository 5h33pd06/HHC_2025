import os
import requests
from urllib.parse import urlparse

def download_files(url_file, output_folder):
    # 1. Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created directory: {output_folder}")

    # 2. Open the text file containing the URLs
    try:
        with open(url_file, 'r') as file:
            urls = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{url_file}' was not found.")
        return

    print(f"Found {len(urls)} URLs. Starting download...")
    print("-" * 30)

    # 3. Iterate through each URL
    for url in urls:
        url = url.strip() # Remove whitespace/newlines
        
        if not url:
            continue # Skip empty lines

        try:
            # Extract filename from URL (e.g., http://site.com/image.png -> image.png)
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            
            # Fallback if no filename is found in URL
            if not filename:
                filename = "downloaded_file"

            save_path = os.path.join(output_folder, filename)

            # 4. Make the request
            # stream=True is important for large files so we don't load the whole file into RAM
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status() # Check for HTTP errors (like 404)

            # 5. Write the file to the disk
            with open(save_path, 'wb') as out_file:
                for chunk in response.iter_content(chunk_size=8192):
                    out_file.write(chunk)
            
            print(f"[SUCCESS] Saved: {filename}")

        except requests.exceptions.HTTPError as err:
            print(f"[ERROR] Bad Status for {url}: {err}")
        except requests.exceptions.ConnectionError:
            print(f"[ERROR] Connection failed for {url}")
        except Exception as e:
            print(f"[ERROR] General error for {url}: {e}")

    print("-" * 30)
    print("Batch download complete.")

# --- Configuration ---
if __name__ == "__main__":
    # Name of your text file with URLs
    TXT_FILE = "gnome_dl.txt"
    # Name of the folder where files will be saved
    DOWNLOAD_DIR = "licenses"

    download_files(TXT_FILE, DOWNLOAD_DIR)