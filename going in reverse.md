# Going in Reverse
<img src="./images/media/image121.jpeg" />

Talking with Kevin, we get some insight into this challenge.

<img src="./images/media/image122.png"/>


We also pick up a C64 basic program:

<img src="./images/media/image123.png" /> 

The provided source code is a BASIC program that implements a simple
password check.

Lines 20-30: Define two encrypted string variables: ENC\_PASS$ (Password) and ENC\_FLAG$ (The Flag).

Lines 40-50: Takes user input and checks the length against the encrypted password.

Line 70 (The Vulnerability): The program iterates through the user input character by character. It takes the ASCII (PETSCII) value of the character, performs an XOR 7 operation, and checks if it matches the stored encrypted string. CHR$(ASC(MID$(PASS$,I,1)) XOR 7)

<img src="./images/media/image124.png" />

Because the XOR operation is symmetric, we do not need to bruteforce the password. We can simply apply the same operation (XOR 7) to the stored ciphertext strings (ENC\_PASS$ and ENC\_FLAG$) to recover the plaintext.

2\. Manual Decryption  
Key: 7 (Binary 0000 0111)  
Target 1: The Password (ENC\_PASS$)  
Ciphertext: D13URKBT  
Decrypted Password: C64RULES

<img src="./images/media/image125.png" />

Target 2: The Flag (ENC\_FLAG$)

Ciphertext: DSA|auhts\*wkfi=dhjwubtthut+dhhkfis+hnkz  
  
We apply the same logic and we get our decrypted flag! We can do it all manually, write a python script, or we can also use CyberChef to decode the messages.

<img src="./images/media/image126.png"/>
