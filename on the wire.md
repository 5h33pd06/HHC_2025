# On the Wire
<img src="./images/media/image267.png" />

When we click on the robot terminal next to Evan, we get an up close view of the robot, and we can see the robot has an oscilloscope which we can see the different frequencies in use.

<img src="./images/media/image268.jpeg" />

-   **1-Wire bus (dq)**

-   **SPI bus (mosi, sck)**

-   **I²C bus (sda, scl)**

Each protocol hides information needed to decode the next stage, creating a multi-layer pipeline:

1.  **Decode 1-Wire** → extract the **SPI XOR key**

2.  **Decode SPI** → extract the **I²C XOR key** and the target device address

3.  **Decode I²C** → decrypt the temperature value from device 0x3C

**Data Acquisition**

Using BurpSuite, we can capture all of the traffic and we see that we have five live WebSocket endpoints:

<img src="./images/media/image269.png"/>

/wire/dq → 1-Wire data line

/wire/sck → SPI clock

/wire/mosi → SPI MOSI

/wire/scl → I2C clock

/wire/sda → I2C data

Each stream consists of JSON frames:

{"line": "dq", "t": 1577, "v": 1}

-   t = integer timestamp (µs units in this system)

-   v = logical level (0/1)

From here, there are a few ways we can complete this challenge. For those who like to visualize, we can capture the signals with a custom Python capture script (capture\_threaded.py) that opens 5 WebSocket clients in parallel and writes each signal as a text file, and then use another custom script called convert\_to\_vcd.py to convert those text files into one single VCD file that can be imported into a tool like PulseView. 

<img src="./images/media/image270.png" />
<img src="./images/media/image272.png" />

We can also use a strictly scripted approach and create a script (capture\_signals.py) that writes all of the signals out as .jsonl files for offline decoding. We can let the capture run for as long as we want, but we only need to let it run for about two minutes for the best results.

<img src="./images/media/image271.png"/>

**Stage 1 — Decode 1-Wire to Recover the SPI XOR Key**

**1-Wire Protocol Characteristics**

-   **LSB-first** bit order

-   Data is encoded via **pulse width**, not clocked edges

    -   Short low pulse → logical 1 (or 0 depending on device)

    -   Long low pulse → logical 0 (or 1)

-   Frames begin with a **reset pulse**, followed by presence and data slots

The raw dq.jsonl data contained thousands of low-pulse segments. We extracted all low pulses and inspected their durations:

Pulse durations &lt; 100 µs: \[6, 60\]  
Threshold: 33 µs  
Short pulse = ~6 µs  
Long pulse = ~60 µs

We grouped pulses into frames using the reset markers the challenge conveniently inserts.

**Brute-Forcing Bit Mapping and Byte Alignment**

Because:

-   1-Wire is LSB-first

-   We don’t yet know if short=0 or short=1

-   The bitstream may not begin at a byte boundary

We brute-forced:

-   both mappings (short→0/1)

-   all 8 possible bit offsets

We scored each decoding by ASCII "printability."

The highest-scoring frame produced:

.read and decrypt the SPI bus data using the XOR key: icy

**Stage 1 Output**

<table>
<colgroup>
<col style="width: 63%" />
<col style="width: 36%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>SPI XOR key</strong></th>
<th>icy</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**Stage 2 — Decode SPI Bus and Recover the I²C XOR Key + Target
Address**

**SPI Protocol Characteristics**

-   SPI uses separate clock (sck) and data (mosi) lines

-   **MSB-first** bit order

-   Data is sampled on the **rising edge** of SCK

We merged SCK and MOSI event streams, tracked MOSI’s value, and captured bits whenever SCK transitioned from 0→1.

This yielded a bitstream which we grouped into 8-bit MSB-first bytes. The first 100 decrypted bytes (using XOR key icy) clearly formed human-readable ASCII:

read and decrypt the I2C bus data using the XOR key: bananza. The temperature sensor address is 0x3C

**Stage 2 Output**

<table>
<colgroup>
<col style="width: 66%" />
<col style="width: 33%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>Item</strong></th>
<th><strong>Value</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><strong>I²C XOR key</strong></td>
<td>bananza</td>
</tr>
<tr class="even">
<td><strong>I²C target address</strong></td>
<td>0x3C</td>
</tr>
</tbody>
</table>

**Stage 3 — Decode the I²C Bus and Recover the Temperature**

Our initial attempt at a full I²C state machine (START/STOP detection) produced no complete bytes. The sampling interval was fast, but START/STOP edges were not cleanly detectable.

**Solution: Brute-Force I²C Frame Alignment**

<img src="./images/media/image273.png"/>

If we use the custom script solver.py, we’ll see all 3 stages carried out and then our final solution displayed at the bottom.

I²C frames always follow this repeating pattern:

\[8 data bits MSB-first\] \[1 ACK bit\]

So we:

1.  Sampled SDA on **every rising edge of SCL**

2.  Obtained a raw bitstream of **247 bits**

3.  Tried decoding using all **bit offsets 0–8**

4.  Checked each decoded byte stream for occurrences of:

    -   0x78 (address=0x3C, write)

    -   0x79 (address=0x3C, read)

Offset **1** produced valid address bytes:

Address @ index 4 = 0x78 (WRITE)

We extracted the next 16 bytes as the encrypted payload:

**I²C Encrypted Payload**

51 53 40 59 5A D1 29 28 2F 29 27 09 18 01 54 15

**Decrypted Payload (XOR with 'bananza')**

33 32 2E 38 34 AB 48 4A 4E 47 46 67 62 60 36 74

We are closing in on the end of the HHC and getting closer to saving
Christmas! Let’s head back over to the Retro Store and talk to Goose
Olivia.
