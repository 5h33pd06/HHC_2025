# Visual Firewall

<img src="./images/media/image89.png" />

<img src="./images/media/image90.jpeg" />

If we head up to the Netwars room in the Grand Hotel, we can talk to Chris Elgee for our Visual Firewall challenge.

We can click on the firewall server rack and then we’re presented with the webpage for the Holiday Firewall Simulator.

<img src="./images/media/image91.png" />

This exercise presents firewall configuration in a good way that’s easy to understand. We have a graphical interface that we can interact with and see the logical flow of traffic between all parts of the network. We are tasked with creating filters for Internet to DMZ, DMZ to Internal, Internal to DMZ, Internal to Cloud, Internal to Workstations, and ensuring that Direct internet to internal access is blocked.

<img src="./images/media/image92.png"/>

We can click on each of the icons in the network diagram and then make the appropriate changes to the configuration.

<img src="./images/media/image93.png"/>

If we click on Internet, we can allow HTTPS Port 443 and HTTP Port 80 for connections to the DMZ.

<img src="./images/media/image94.png" />

Next, we can click on DMZ and allow HTTP Port 80, HTTPS Port 443, and SSH Port 22.

<img src="./images/media/image95.png"/>

Next we can click on Internal Network and allow HTTP Port 80, HTTPS Port 443, SMTP Port 25, and SSH Port 22 to Cloud Services.

We then want to allow all ports for connection to Workstations.

Once all of these configurations are made, we should see each one show completed at the top, and then we receive our Victory for making all of the correct configurations!

<img src="./images/media/image96.png" />
