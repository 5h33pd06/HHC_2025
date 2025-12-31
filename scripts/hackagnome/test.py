#!/usr/bin/python3
import can
import time
import sys

# Configure your interface
IFACE_NAME = "gcan0"

def main():
    try:
        bus = can.interface.Bus(channel=IFACE_NAME, interface='socketcan')
        print(f"Connected to {IFACE_NAME}.")
    except Exception as e:
        print(f"Error connecting: {e}")
        sys.exit(1)

    print("\n--- MANUAL MAPPING MODE ---")
    print("Press the number keys to fire the corresponding CAN ID.")
    print("Watch the GnomeBot to see which direction it moves.")
    print("---------------------------")
    print("1: Send 0x201")
    print("2: Send 0x202")
    print("3: Send 0x203")
    print("4: Send 0x204")
    print("q: Quit")
    print("---------------------------")

    while True:
        choice = input("Command > ").strip().lower()

        if choice == 'q':
            break
        
        target_id = None
        
        if choice == '1': target_id = 0x201
        elif choice == '2': target_id = 0x202
        elif choice == '3': target_id = 0x203
        elif choice == '4': target_id = 0x204
        
        if target_id:
            msg = can.Message(arbitration_id=target_id, data=[], is_extended_id=False)
            try:
                bus.send(msg)
                print(f" -> SENT: 0x{target_id:X}")
            except can.CanError as e:
                print(f"Error sending: {e}")
        else:
            print("Invalid key.")

    bus.shutdown()

if __name__ == "__main__":
    main()
