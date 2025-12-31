#!/usr/bin/env python3
import json
import re
import argparse
from pathlib import Path

# ------------------------
# Common helpers
# ------------------------

def ascii_preview(data_bytes, limit=120):
    chars = []
    for b in data_bytes[:limit]:
        if 0x20 <= b <= 0x7E:
            chars.append(chr(b))
        elif b in (0x09, 0x0A, 0x0D):
            chars.append(chr(b))
        else:
            chars.append(".")
    return "".join(chars)

def score_printable(data_bytes):
    if not data_bytes:
        return 0.0
    printable = 0
    for b in data_bytes:
        if 0x20 <= b <= 0x7E or b in (0x09, 0x0A, 0x0D):
            printable += 1
    return printable / len(data_bytes)

def xor_with_key(data_bytes, key_str):
    key_bytes = key_str.encode("ascii")
    out = bytearray()
    for i, b in enumerate(data_bytes):
        out.append(b ^ key_bytes[i % len(key_bytes)])
    return bytes(out)

# ------------------------
# Stage 1 . 1 Wire (dq) → SPI key
# ------------------------

def load_dq_events(path):
    events = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("line") != "dq":
                continue
            if "t" not in obj or "v" not in obj:
                continue
            events.append(obj)
    events.sort(key=lambda e: e["t"])
    return events

def extract_low_pulses(events):
    pulses = []
    for i in range(len(events) - 1):
        cur = events[i]
        nxt = events[i + 1]
        if cur["v"] == 0:
            dt = nxt["t"] - cur["t"]
            if dt <= 0:
                continue
            pulses.append({
                "start": cur["t"],
                "duration": dt,
                "marker": cur.get("marker")
            })
    return pulses

def find_data_threshold(pulses, max_data_width=100.0):
    data_widths = sorted(p["duration"] for p in pulses if p["duration"] < max_data_width)
    if len(data_widths) < 2:
        raise RuntimeError("Not enough data pulses to determine threshold")
    best_gap = 0
    best_index = 0
    for i in range(len(data_widths) - 1):
        gap = data_widths[i + 1] - data_widths[i]
        if gap > best_gap:
            best_gap = gap
            best_index = i
    short_max = data_widths[best_index]
    long_min = data_widths[best_index + 1]
    threshold = (short_max + long_min) / 2.0
    return threshold, short_max, long_min, sorted(set(data_widths))

def split_frames_by_reset(pulses):
    frames = []
    current = []
    for p in pulses:
        if p.get("marker") == "reset":
            if current:
                frames.append(current)
                current = []
            continue
        current.append(p)
    if current:
        frames.append(current)
    return frames

def pulses_to_bit_kinds(frame_pulses, threshold, max_data_width=100.0):
    kinds = []
    for p in frame_pulses:
        dt = p["duration"]
        if dt >= max_data_width:
            continue
        kind = "short" if dt < threshold else "long"
        kinds.append(kind)
    return kinds

def bits_to_bytes_lsb(bits_kinds, short_value, long_value, bit_offset):
    bits = []
    for k in bits_kinds:
        bits.append(short_value if k == "short" else long_value)
    if bit_offset > 0:
        bits = bits[bit_offset:]
    bytes_out = []
    cur = 0
    pos = 0
    for b in bits:
        cur |= (b & 1) << pos
        pos += 1
        if pos == 8:
            bytes_out.append(cur)
            cur = 0
            pos = 0
    return bytes_out

def stage1_get_spi_key(dq_path):
    print("[*] Stage 1 . decoding 1 Wire dq to get SPI key")
    events = load_dq_events(dq_path)
    print(f"    Loaded {len(events)} dq events")
    pulses = extract_low_pulses(events)
    print(f"    Extracted {len(pulses)} low pulses")
    threshold, short_max, long_min, widths = find_data_threshold(pulses)
    print(f"    Pulse widths <100: {widths}")
    print(f"    threshold={threshold:.2f}, short_max={short_max}, long_min={long_min}")

    frames = split_frames_by_reset(pulses)
    print(f"    Found {len(frames)} frames based on reset markers")

    best_frame = None
    best_score = -1.0
    best_bytes = None
    best_preview = ""
    for fi, frame in enumerate(frames):
        kinds = pulses_to_bit_kinds(frame, threshold)
        if not kinds:
            continue
        for offset in range(8):
            for mapping_name, short_val, long_val in [
                ("short=0,long=1", 0, 1),
                ("short=1,long=0", 1, 0),
            ]:
                bts = bits_to_bytes_lsb(kinds, short_val, long_val, offset)
                if not bts:
                    continue
                score = score_printable(bts)
                if score > best_score:
                    best_score = score
                    best_frame = (fi, offset, mapping_name)
                    best_bytes = bts
                    best_preview = ascii_preview(bts)

    if best_bytes is None:
        raise RuntimeError("Failed to decode any frame from dq")

    fi, offset, mapping_name = best_frame
    print(f"    Best frame={fi}, offset={offset}, mapping={mapping_name}, printable={best_score:.3f}")
    print("    ASCII preview (first 120 chars):")
    print("    " + best_preview)

    # Extract SPI key from text
    text = "".join(chr(b) if 0x20 <= b <= 0x7E or b in (0x09,0x0A,0x0D) else " " for b in best_bytes)
    m = re.search(r"XOR key:\s*([A-Za-z0-9_]+)", text, re.IGNORECASE)
    if not m:
        raise RuntimeError("Could not find SPI XOR key in 1 Wire text")
    spi_key = m.group(1)
    print(f"    Recovered SPI XOR key: {spi_key}")
    return spi_key

# ------------------------
# Stage 2 . SPI (sck+mosi) → I2C key + address
# ------------------------

def load_line_events(path, line_name):
    events = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("line") != line_name or "t" not in obj or "v" not in obj:
                continue
            events.append({"t": obj["t"], "v": obj["v"], "line": line_name})
    events.sort(key=lambda e: e["t"])
    return events

def merge_events(ev_a, ev_b):
    all_ev = ev_a + ev_b
    all_ev.sort(key=lambda e: e["t"])
    return all_ev

def sample_spi_bits(all_events):
    sck = 0
    mosi = 0
    bits = []
    for ev in all_events:
        if ev["line"] == "mosi":
            mosi = ev["v"]
        elif ev["line"] == "sck":
            prev = sck
            sck = ev["v"]
            if prev == 0 and sck == 1:
                bits.append(mosi)
    return bits

def bits_to_bytes_msb(bits):
    if not bits:
        return []
    usable = len(bits) - (len(bits) % 8)
    bits = bits[:usable]
    out = []
    for i in range(0, len(bits), 8):
        val = 0
        for bit in bits[i:i+8]:
            val = (val << 1) | (bit & 1)
        out.append(val)
    return out

def stage2_get_i2c_key_and_addr(sck_path, mosi_path, spi_key):
    print("[*] Stage 2 . decoding SPI to get I2C key and address")
    sck_events = load_line_events(sck_path, "sck")
    mosi_events = load_line_events(mosi_path, "mosi")
    print(f"    Loaded {len(sck_events)} SCK and {len(mosi_events)} MOSI events")
    all_events = merge_events(sck_events, mosi_events)
    bits = sample_spi_bits(all_events)
    print(f"    Sampled {len(bits)} bits on SPI")
    spi_bytes = bits_to_bytes_msb(bits)
    print(f"    Built {len(spi_bytes)} SPI bytes")

    if not spi_bytes:
        raise RuntimeError("No SPI bytes decoded")

    print("    SPI encrypted ASCII preview:")
    print("    " + ascii_preview(spi_bytes))

    decrypted = xor_with_key(spi_bytes, spi_key)
    text = "".join(chr(b) if 0x20 <= b <= 0x7E or b in (0x09,0x0A,0x0D) else " " for b in decrypted)
    print("    SPI decrypted ASCII preview:")
    print("    " + ascii_preview(decrypted))

    m_key = re.search(r"XOR key:\s*([A-Za-z0-9_]+)", text, re.IGNORECASE)
    if not m_key:
        raise RuntimeError("Could not find I2C XOR key in SPI text")
    i2c_key = m_key.group(1)

    m_addr = re.search(r"address is\s*(0x[0-9A-Fa-f]+)", text, re.IGNORECASE)
    if not m_addr:
        raise RuntimeError("Could not find I2C address in SPI text")
    addr_str = m_addr.group(1)
    addr_val = int(addr_str, 16)

    print(f"    Recovered I2C XOR key: {i2c_key}")
    print(f"    I2C target address: {addr_str} (decimal {addr_val})")
    return i2c_key, addr_val

# ------------------------
# Stage 3 . I2C (sda+scl) → temperature
# ------------------------

def sample_i2c_bits(all_events):
    sda = 1
    scl = 1
    bits = []
    for ev in all_events:
        if ev["line"] == "sda":
            sda = ev["v"]
        elif ev["line"] == "scl":
            prev = scl
            scl = ev["v"]
            if prev == 0 and scl == 1:
                bits.append(sda)
    return bits

def decode_bytes_with_offset(bits, offset):
    bytes_out = []
    i = offset
    n = len(bits)
    while i + 8 <= n:
        val = 0
        for b in bits[i:i+8]:
            val = (val << 1) | (b & 1)
        bytes_out.append(val)
        i += 9
    return bytes_out

def stage3_get_temperature(sda_path, scl_path, i2c_key, addr_val):
    print("[*] Stage 3 . decoding I2C to get temperature")
    sda_events = load_line_events(sda_path, "sda")
    scl_events = load_line_events(scl_path, "scl")
    print(f"    Loaded {len(sda_events)} SDA and {len(scl_events)} SCL events")
    all_events = merge_events(sda_events, scl_events)
    bits = sample_i2c_bits(all_events)
    print(f"    Sampled {len(bits)} I2C bits")

    addr_write = (addr_val << 1) | 0
    addr_read = (addr_val << 1) | 1

    # find best offset
    candidates = []
    for offset in range(9):
        dec = decode_bytes_with_offset(bits, offset)
        hits = sum(1 for b in dec if b in (addr_write, addr_read))
        candidates.append((offset, len(dec), hits))
    print("    Offset scan (offset, total_bytes, hits_of_addr_write/read):")
    for o, total, hits in candidates:
        print(f"      offset={o}: total={total}, hits={hits}")
    best_offset, total, hits = max(candidates, key=lambda x: x[2])
    print(f"    Best offset={best_offset}, total_bytes={total}, hits={hits}")
    if hits == 0:
        raise RuntimeError("No address hits found in I2C stream")

    stream_bytes = decode_bytes_with_offset(bits, best_offset)
    print(f"    Decoded {len(stream_bytes)} bytes at offset {best_offset}")

    # find first instance of our address, prefer READ
    idx_target = None
    direction = None
    for i, b in enumerate(stream_bytes):
        if b == addr_read:
            idx_target = i
            direction = "READ"
            break
    if idx_target is None:
        for i, b in enumerate(stream_bytes):
            if b == addr_write:
                idx_target = i
                direction = "WRITE"
                break
    if idx_target is None:
        raise RuntimeError("Could not find address byte in decoded stream")

    print(f"    Found address byte at index {idx_target} ({direction})")

    # assume following bytes contain encrypted temp string
    window = 16
    payload = stream_bytes[idx_target + 1: idx_target + 1 + window]
    if not payload:
        raise RuntimeError("No payload bytes after address for temperature")

    decrypted = xor_with_key(payload, i2c_key)
    print("    Decrypted I2C payload ASCII preview:")
    print("    " + ascii_preview(decrypted))

    text = "".join(chr(b) if 0x20 <= b <= 0x7E or b in (0x09,0x0A,0x0D) else " " for b in decrypted)
    m_temp = re.search(r"([0-9]+(?:\.[0-9]+)?)", text)
    if not m_temp:
        raise RuntimeError("Could not parse temperature value from decrypted payload")
    temp_str = m_temp.group(1)
    return float(temp_str), text.strip()

# ------------------------
# Main
# ------------------------

def main():
    parser = argparse.ArgumentParser(
        description="One shot decoder . 1 Wire → SPI → I2C → final temperature"
    )
    parser.add_argument(
        "--dir",
        default="captures",
        help="Directory containing dq.jsonl, sck.jsonl, mosi.jsonl, sda.jsonl, scl.jsonl (default: captures)"
    )
    args = parser.parse_args()
    base = Path(args.dir)

    dq_path = base / "dq.jsonl"
    sck_path = base / "sck.jsonl"
    mosi_path = base / "mosi.jsonl"
    sda_path = base / "sda.jsonl"
    scl_path = base / "scl.jsonl"

    for p in [dq_path, sck_path, mosi_path, sda_path, scl_path]:
        if not p.exists():
            raise SystemExit(f"Missing required capture file: {p}")

    spi_key = stage1_get_spi_key(dq_path)
    i2c_key, addr_val = stage2_get_i2c_key_and_addr(sck_path, mosi_path, spi_key)
    temp_value, temp_text = stage3_get_temperature(sda_path, scl_path, i2c_key, addr_val)

    print()
    print("========================================")
    print(f"SPI XOR key   : {spi_key}")
    print(f"I2C XOR key   : {i2c_key}")
    print(f"I2C address   : 0x{addr_val:02X}")
    print(f"Temperature   : {temp_value}")
    print(f"Payload text  : {temp_text}")
    print("========================================")

if __name__ == "__main__":
    main()
