import websocket
import threading
import os
import time

# Configuration
OUTPUT_DIR = "captured_signals"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Endpoints mapping
ENDPOINTS = {
    "i2c_sda": "wss://signals.holidayhackchallenge.com/wire/sda",
    "i2c_scl": "wss://signals.holidayhackchallenge.com/wire/scl",
    "onewire_dq": "wss://signals.holidayhackchallenge.com/wire/dq",
    "spi_mosi": "wss://signals.holidayhackchallenge.com/wire/mosi",
    "spi_sck": "wss://signals.holidayhackchallenge.com/wire/sck"
}

# Headers and Cookies from your Burp capture
# formatting as a list for websocket-client
HEADERS = [
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "Origin: https://signals.holidayhackchallenge.com",
    "Accept-Encoding: gzip, deflate, br",
    "Accept-Language: en-US,en;q=0.9",
    "Cookie: _ga=GA1.1.260030523.1731015958; _ga_F6ZZNPR5E5=GS1.1.1731435373.13.1.1731435511.0.0.0"
]

def on_message(ws, message):
    # The 'ws.filename' is a custom attribute we will attach to the object
    with open(ws.filename, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")

def on_error(ws, error):
    print(f"[-] Error on {ws.name}: {error}")

def on_open(ws):
    print(f"[+] Connected to {ws.name}")

def start_socket(name, url):
    filename = os.path.join(OUTPUT_DIR, f"{name}.txt")
    
    # Enable trace to see debug info if needed
    # websocket.enableTrace(True)
    
    ws = websocket.WebSocketApp(
        url,
        header=HEADERS,
        on_message=on_message,
        on_error=on_error,
        on_open=on_open
    )
    
    # Attach custom attributes so we know which file to write to inside the callback
    ws.name = name
    ws.filename = filename
    
    # Run the socket (this blocks, so we run it in a thread)
    ws.run_forever()

if __name__ == "__main__":
    print("Starting threaded capture. Press Ctrl+C to stop...")
    threads = []
    
    try:
        # Launch a thread for each endpoint
        for name, url in ENDPOINTS.items():
            t = threading.Thread(target=start_socket, args=(name, url))
            t.daemon = True # Kills threads when main program exits
            t.start()
            threads.append(t)
            time.sleep(0.1) # Stagger start slightly
        
        # Keep the main thread alive to allow Ctrl+C
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n[*] Stopping capture...")
