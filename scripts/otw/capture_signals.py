#!/usr/bin/env python3
import asyncio
import datetime
import json
import argparse
import pathlib
import signal
import sys
import websockets
WIRE_ENDPOINTS = {
    "dq":  "wss://signals.holidayhackchallenge.com/wire/dq",
    "sck": "wss://signals.holidayhackchallenge.com/wire/sck",
    "mosi":"wss://signals.holidayhackchallenge.com/wire/mosi",
    "scl": "wss://signals.holidayhackchallenge.com/wire/scl",
    "sda": "wss://signals.holidayhackchallenge.com/wire/sda",
}
async def capture_wire(name: str,
                       url: str,
                       outdir: pathlib.Path,
                       stop_event: asyncio.Event) -> None:
    """
    Connects to a single WebSocket endpoint and streams all messages
    to <outdir>/<name>.jsonl as one JSON object per line.
    Automatically reconnects on errors until stop_event is set.
    """
    outfile = outdir / f"{name}.jsonl"
    outfile.parent.mkdir(parents=True, exist_ok=True)
    print(f"[{name}] Starting. URL={url}  Output={outfile}")
    while not stop_event.is_set():
        try:
            # Plain connect; no extra_headers so it works with older websockets versions
            async with websockets.connect(url) as ws:
                print(f"[{name}] Connected")
                async for msg in ws:
                    # Server should send JSON text like {"line": "...", "t": ..., "v": ...}
                    try:
                        data = json.loads(msg)
                    except json.JSONDecodeError:
                        # Fall back to wrapping raw payload
                        data = {"raw": msg}
                    # Ensure line field exists, and add local capture timestamp
                    data.setdefault("line", name)
                    data["capture_ts"] = datetime.datetime.utcnow().isoformat() + "Z"
                    with outfile.open("a", encoding="utf-8") as f:
                        f.write(json.dumps(data) + "\n")
                    if stop_event.is_set():
                        break
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"[{name}] Error: {e!r}. Reconnecting in 2 seconds.", file=sys.stderr)
            await asyncio.sleep(2)
    print(f"[{name}] Stopped.")
def setup_signal_handlers(stop_event: asyncio.Event):
    """
    Allow Ctrl+C to stop all capture tasks cleanly.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return
    def handler():
        if not stop_event.is_set():
            print("\n[main] Ctrl+C received. Stopping capture.")
            stop_event.set()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, handler)
        except NotImplementedError:
            # On Windows, add_signal_handler may not be available
            pass
async def run_capture(duration: float | None,
                      outdir: pathlib.Path) -> None:
    stop_event = asyncio.Event()
    setup_signal_handlers(stop_event)
    tasks = []
    for name, url in WIRE_ENDPOINTS.items():
        tasks.append(asyncio.create_task(
            capture_wire(name, url, outdir, stop_event)
        ))
    async def timer():
        if duration is not None:
            try:
                await asyncio.sleep(duration)
            finally:
                print(f"[main] Duration {duration} seconds reached. Stopping.")
                stop_event.set()
    if duration is not None:
        tasks.append(asyncio.create_task(timer()))
    # Wait for all tasks to finish
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        pass
    print("[main] All capture tasks finished.")
def parse_args():
    parser = argparse.ArgumentParser(
        description="Capture Holiday Hack signal WebSockets to JSONL files."
    )
    parser.add_argument(
        "-d", "--duration",
        type=float,
        default=60.0,
        help="Capture duration in seconds. Use 0 or negative for infinite (until Ctrl+C). Default: 60."
    )
    parser.add_argument(
        "-o", "--outdir",
        type=str,
        default="captures",
        help="Output directory for JSONL files. Default: ./captures"
    )
    return parser.parse_args()
def main():
    args = parse_args()
    if args.duration is not None and args.duration <= 0:
        duration = None
    else:
        duration = args.duration
    outdir = pathlib.Path(args.outdir)
    try:
        asyncio.run(run_capture(duration, outdir))
    except KeyboardInterrupt:
        print("\n[main] KeyboardInterrupt, exiting.")
if __name__ == "__main__":
    main()
