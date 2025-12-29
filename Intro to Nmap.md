# Intro to Nmap
<img src="./images/media/image51.png"/>

<img src="./images/media/image52.jpeg"/>

If we head up to the parking lot of the Grand Hotel, we meet Eric Pursley for a Nmap challenge.

<img src="./images/media/image53.png" />

Nmap is a great recon and enumeration tool. Mastering some basic commands and functionality should be one of the first thing any good security analyst should do!

<img src="./images/media/image54.png" />  
<img src="./images/media/image55.png" />

For this question, we simply run <span class="mark">nmap 127.0.12.25</span> to perform a basic scan of the top 1000 ports (not 1-1000, but the top 1000 most commonly used). We see that port 8080 is open.

<img src="./images/media/image56.png"/>

Next, we need to run a full port scan on all 65535 ports by doing <span class="mark">nmap -p- 127.0.12.25</span> which shows us that port 24601 is open and running an unknown service. Sometimes these ports are nothing for us to do anything with, however they can also be used to obscure activity.   
  
We are next asked to scan an ip range for 127.0.12.20-127.0.12.28 and see which system has a port open. We’ll use <span class="mark">nmap -p- 127.0.12.20-28</span> to search all ports on all of these endpoints, which shows that 127.0.12.23 has port 8080 open.

<img src="./images/media/image57.png"/>
<img src="./images/media/image58.png"/>
We are next asked to see what service is running on 127.0.12.23:8080. We do this by using <span class="mark">nmap -p 8080 -sV 127.0.12.25</span>. This tells nmap to search only port 8080 and to use -sV to send protocol-specific probes to try to identify the application/service, version number, and the underlying protocol.

<img src="./images/media/image59.png" />
Next, we are asked to interact with the first port we found, 127.0.12.25:24601 by using the Ncat (netcat) command.

When using netcat, we specify the target host first and then the port, separated by spaces. So, to connect and interact with 127.0.12.25:24601, we will use <span class="mark">nc 127.0.12.25 24601</span> which connects us to the WarDriver 9000 interface!
