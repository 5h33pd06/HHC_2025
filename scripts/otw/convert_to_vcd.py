import os
import json
import sys

# Configuration
INPUT_DIR = "captured_signals"
OUTPUT_FILE = "signals.vcd"
TIMESCALE = "1us"  # Microseconds usually work best for these challenges

# Map filenames to VCD variables
# (filename_no_ext, vcd_symbol, signal_name)
SIGNALS = [
    ("i2c_sda", "!", "SDA"),
    ("i2c_scl", "@", "SCL"),
    ("onewire_dq", "#", "DQ"),
    ("spi_mosi", "$", "MOSI"),
    ("spi_sck", "%", "SCK"),
]

def parse_line(line):
    """
    Attempts to extract (timestamp, value) from a JSON line.
    Adjusts keys based on common CTF signal formats.
    """
    try:
        data = json.loads(line.strip())
        
        # HHC often uses 'tick', 'time', or 't' for timestamp
        timestamp = data.get('tick') or data.get('time') or data.get('t')
        
        # HHC often uses 'state', 'value', 'v', or 'l' for level
        value = data.get('state') or data.get('value') or data.get('v') or data.get('l')
        
        if timestamp is None or value is None:
            return None
            
        return int(timestamp), int(value)
    except (json.JSONDecodeError, ValueError):
        return None

def main():
    print(f"[*] Reading files from {INPUT_DIR}...")
    
    # 1. Read all events into a single list
    all_events = []
    
    for filename_base, symbol, signal_name in SIGNALS:
        path = os.path.join(INPUT_DIR, f"{filename_base}.txt")
        if not os.path.exists(path):
            print(f"[-] Warning: {path} not found. Skipping.")
            continue
            
        print(f"    Processing {filename_base}...")
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parsed = parse_line(line)
                if parsed:
                    ts, val = parsed
                    # Store tuple: (timestamp, symbol, value)
                    all_events.append((ts, symbol, val))

    if not all_events:
        print("[!] No valid data found. Check your captured files!")
        return

    # 2. Sort events by timestamp
    print("[*] Sorting events...")
    all_events.sort(key=lambda x: x[0])
    
    # 3. Normalize timestamps (start at t=0)
    start_time = all_events[0][0]
    
    # 4. Write VCD Header
    print(f"[*] Writing {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w') as f:
        # Header info
        f.write("$date Today $end\n")
        f.write("$version HHC_Signal_Converter 1.0 $end\n")
        f.write(f"$timescale {TIMESCALE} $end\n")
        f.write("$scope module logic $end\n")
        
        # Define signals
        for _, symbol, name in SIGNALS:
            f.write(f"$var wire 1 {symbol} {name} $end\n")
        
        f.write("$upscope $end\n")
        f.write("$enddefinitions $end\n")
        f.write("$dumpvars\n")
        
        # Initial state (optional, defaulting to 0)
        for _, symbol, _ in SIGNALS:
            f.write(f"0{symbol}\n")
        f.write("$end\n")
        
        # 5. Write Data
        current_time = -1
        for ts, symbol, val in all_events:
            normalized_ts = ts - start_time
            
            # If time advanced, write new timestamp
            if normalized_ts > current_time:
                f.write(f"#{normalized_ts}\n")
                current_time = normalized_ts
            
            # Write signal change
            f.write(f"{val}{symbol}\n")

    print(f"[+] Done! Open {OUTPUT_FILE} in PulseView.")

if __name__ == "__main__":
    main()
