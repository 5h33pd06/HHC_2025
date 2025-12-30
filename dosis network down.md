# Dosis Network Down

<img src="./images/media/image145.jpeg"/>

<img src="./images/media/image146.png" />

Initial enumeration shows that this router is an Archer AX1800 running firmware version 1.14 Build 20230219. If we search online, we find that this is vulnerable under CVE-2023-1389 and has a POC script

<https://www.exploit-db.com/exploits/51677>

<img src="./images/media/image147.jpeg" />

<img src="./images/media/image148.png" />

This attack can be done with a script to get a reverse shell, however we can actually do all of this from within the browser or Burp Repeater.

Using the vulnerable endpoint and writing into the "country" field, we can use simple linux commands to navigate the target and find what we want.

<img src="./images/media/image150.png" />

If we navigate to /etc/config we see that we can view the wireless config file, and we see that the wi-fi password is right there.

Okay, we’re all fueled up to push through the rest of the challenges and got Janusz back into the network. Now let’s get our steps in and head over to the park for a bit of fresh air and talk with Paul.

<img src="./images/media/image149.png" />
