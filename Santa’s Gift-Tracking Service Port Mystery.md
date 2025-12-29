# Santa’s Gift-Tracking Service Port Mystery
<img src="./images/media/image48.png" />

From here, we’ll move east, over towards the Modern Scandinavian. Here we meet Yori Kvitchko who asks for help with Santa’s Gift-Tracker.

<img src="./images/media/image49.png" />

We log into the terminal and are greeted with the challenge information. We are told to us the “ss” tool to identify the port for santa\_tracker and then connect to verify if it’s running.

We are given the first command to try <span class="mark">ss -tlnp</span> which uses “socket statistics” to show us TCP sockets only <span class="mark">-t</span> that are listening <span class="mark">-l</span> and provides numeric output
<span class="mark">-n</span> and the process information <span class="mark">-p</span>

<img src="./images/media/image50.png" />

We see that there is an open port listening on 0.0.0.0:12321!

We can connect to that with the curl command by using <span class="mark">curl localhost:12321</span> to make a simple HTTP request to the service running on port 12321 and print the response in our terminal and then complete our challenge.
