#!/usr/bin/python3
import can
import time

IFACE_NAME = "gcan0"

# Ranges to SKIP (Status messages and Heartbeats)
SKIP_RANGES = [
    range(0x300, 0x401), # Covers 0x300 - 0x400
    range(0x400, 0x4D0)  # Covers 0x400 - 0x4CF
]

def is_skipped(arbitration_id):
    for r in SKIP_RANGES:
        if arbitration_id in r:
            return True
    return False

def scan_can_bus():
    try:
        bus = can.interface.Bus(channel=IFACE_NAME, interface='socketcan')
        print(f"Connected to {IFACE_NAME}. Scanning for HIDDEN commands...")
    except Exception as e:
        print(f"Error: {e}")
        return

    # Focus scan on 0x000 to 0x300 and 0x500 to 0x660
    target_ids = list(range(0x000, 0x300)) + list(range(0x500, 0x660))

    for arbitration_id in target_ids:
        # Don't send to known status IDs
        if is_skipped(arbitration_id):
            continue

        msg = can.Message(arbitration_id=arbitration_id, data=[], is_extended_id=False)
        
        try:
            bus.send(msg)
            
            # Listen briefly for a reply
            start_time = time.time()
            while time.time() - start_time < 0.05:
                rec_msg = bus.recv(timeout=0.01)
                
                if rec_msg and rec_msg.arbitration_id != arbitration_id:
                    # STRICT FILTER: Ignore if the reply is a known background ID
                    if not is_skipped(rec_msg.arbitration_id):
                        print(f"[+] VALID HIT: Sent 0x{arbitration_id:X} -> Got Unique Reply 0x{rec_msg.arbitration_id:X}")
                        break
                    
        except can.CanError:
            pass
        
        time.sleep(0.01)

    print("Scan complete.")

if __name__ == "__main__":
    scan_can_bus()
