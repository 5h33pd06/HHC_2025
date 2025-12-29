# Neighborhood Watch Bypass
<img src="./images/media/image79.jpeg" />

From here, if we head south to the old Datacenter, we’ll meet Kyle Parrish. He lets us know that there’s an issue with the fire alarm but he’s been locked out of the system. If we click on the terminal, we are taken to the CLI for the Fire Alarm system.

<img src="./images/media/image81.jpeg" />
<img src="./images/media/image80.png" />

We see that the system has been placed into Lockout Mode.

<img src="./images/media/image82.png"/>

First, we need to do some general enumeration. We are into challenges that are not holding our hand now, so let’s use the skills we’ve learned so far, along with some we’re bringing into this event!

We can start off by seeing what is in our current directory with a `ls -lah` command. We see a directory called “bin” which contains a link called “runtoanswer” which goes to /etc/firealarm/restore\_fire\_alarm. If we try to run it however, it shows that we don’t have the permission. I didn’t think it would be this easy…

<img src="./images/media/image83.png" />
<img src="./images/media/image84.png" />
If we do some more enumeration, we see that our current user has NOPASSWD sudo privileges on /usr/local/bin/system\_status.sh!!

If we run that script, we see that it shows us the fire alarm system status.

<img src="./images/media/image85.png"/>

If we look at the contents of the script, we see that there are some binaries being called but they don’t have the full paths called out. We can possibly use this to interject our own exploit script to be called instead of the expected binary!

<img src="./images/media/image86.png" />

If we run:

```
echo "User: $(id -u -n) (UID $(id -u))"
echo "$PATH" | tr ':' '\n' | nl -ba
```

this will show us what paths are being looked at and if there any that we can control.

We see that the very first line is “/home/chiuser/bin” which is definitely one that we can control! Let’s see if we can create our own binary executable called “w” since that’s the only one in the script that’s not calling any extra options or modifiers.

We can create the following simple script called “w” in our /home/chiuser/bin directory.

<img src="./images/media/image87.png" />
<img src="./images/media/image88.png" />
This command creates the file called “w” and <span class="mark">&lt;&lt;'EOF'</span> starts a here-document. Everything between this line and the closing <span class="mark">EOF</span> is sent to cat as input. There are ways to make this more robust and less prone to failure, however for simplicity sake, if we use the following simple script that will execute runtoanswer when called:  

```
cat &gt; ~/bin/w &lt;&lt;”EOF”
\#!/usr/bin/env bash``` 
exec runtoanswer “$@”```
EOF
```

We can verify that this has been created in our /home/chiuser/bin directory and make sure that it’s executable by running `chmod +x ~/bin/w` and then we can run our status script as sudo and it should call our exploit script. 

It works!! Instead of running the normal “w” binary, the script calls our exploited “w” which then called the “runtoanswer” link as root and allowed us to regain access!
