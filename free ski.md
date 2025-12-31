# Free Ski
<img src="./images/media/image274.png" />

<img src="./images/media/image275.png" />

We retrieve the FreeSki.exe file from Olivia and when we try to run it, we see that there are some issues. Now, it is entirely possible to find some files to put in for the missing ones and get the program to run and then beat the game, however, as Olivia tells us, “If you ain’t cheatin’, you ain’t tryin’.” So, let’s get to cheatin’!!

The first clue is that FreeSki.exe is a PyInstaller executable. PyInstaller bundles the Python interpreter and script bytecode (.pyc files) into a single .exe. We need to extract the original bytecode. We can use pyinstxtractor.py with command `python pyinstxtractor.py FreeSki.exe` to create a directory named FreeSki\_extracted. Inside, we find FreeSki.pyc. The header of the extracted file indicates this is **Python 3.13** bytecode. This is a very new version of Python, which causes most standard decompilers (like uncompyle6) to fail.

Because Python 3.13 is so new, we cannot easily decompile it back to clean Python source code. Instead, we use **Decompyle++** to disassemble it. This gives us the raw instructions (opcodes) that the Python interpreter executes. We can use command `./pycdas FreeSki.pyc &gt; freeski.txt` to get a readable text file containing the assembly instructions. We can now analyze the logic by reading these instructions.

Searching the text file for the string "Flag" leads us to a function called SetFlag. Inside SetFlag, we see the following logic:

1.  **Seed Calculation:** The code iterates through a list (presumably the treasures collected) and creates a product using XOR operations.

    -   **LOAD\_FAST product, LOAD\_CONST 8, BINARY\_OP (&lt;&lt;) (Left Shift).**

    -   **BINARY\_OP (^) (XOR) with the treasure value.**

<!-- -->

1.  **Seeding RNG:** It passes this product to random.seed.

2.  **Decryption:** It iterates through encoded\_flag , generates a random integer between 0-255 , and XORs it with the encoded flag byte.

To get the correct key, we need to know where the treasures are. Searching for "treasure", we find the Mountain class and a function called GetTreasureLocations.

This function generates the treasure map procedurally:

1.  **The Seed:** It seeds the random generator using a CRC32 checksum of the mountain's **name**.

    -   **LOAD\_ATTR name, LOAD\_ATTR encode, binascii.crc32.**

<!-- -->

1.  **The Loop:** It loops 5 times.

<!-- -->

1.  **Calculations:**

    -   **Elevation (e\_delta): A random integer between 200 and 800.**

    -   **Horizontal (h\_delta): A random integer derived from e\_delta divided by 4.**

<!-- -->

1.  **Storage:** It stores the location in a dictionary where the key is the height and the value is the horizontal location.

**C. Formatting the Key**

Finally, we need to look at main to see how these locations are converted into the list passed to SetFlag. When a collision with a treasure occurs, the code appends a value to treasures\_collected:

-   collided\_row (Elevation) \* mountain\_width (1000) + collided\_row\_offset (Horizontal).

<img src="./images/media/image276.png" />

We can write a Python script to replicate the RNG logic for every mountain found in the file (Aspen, Whistler, Dragonmount, etc.).

Last, but not least, we have now opened up Snowblind Ambush in the Grand Hotel. This will get us our final challenge and an end to Frosty’s evil
plan!
