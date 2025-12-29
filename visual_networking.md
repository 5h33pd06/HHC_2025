# Visual Networking

<img src="./images/media/image8.png" style="width:3.04583in;height:0.96111in" />
As we move around, we see that we have a challenge to the south with Jared Folkins.
<img src="./images/media/image7.jpeg" style="width:2.64236in;height:1.93472in" />

If we click on the terminal, we are presented with a web browser based challenge. Looks like this challenge is all about networking principles. As a one snowflake challenge, this is pretty straightforward and meant to teach. <img src="./images/media/image9.png" style="width:6.5in;height:2.02917in" />

Our first part of the challenge is to “find the IP address of visual-networking.holidayhackchallenge.com” using an IPv4 DNS request.

<img src="./images/media/image10.png" style="width:2.96528in;height:1.51806in" />
Web addresses are resolved using DNS requests which turn IP addresses into names we can remember and vice versa. DNS is what allows us to connect to websites and other services without having to remember each and every IP address of the system we’re connecting to. This also allows for IP address changes behind the scenes to not affect our ability to connect to websites.

We solve this one with by selecting the correct values from the drop-down menus for both the client and DNS Server sides. We are presented with ports 21, 53, 69, and 123.

<table>
<colgroup>
<col style="width: 6%" />
<col style="width: 93%" />
</colgroup>
<tbody>
<tr class="even">
<td>21</td>
<td>FTP – TCP, Unencrypted, sends commands from client to server</td>
</tr>
<tr class="odd">
<td>53</td>
<td>DNS – TCP/UDP, Translates human readable domain names into machine
readable IP addresses</td>
</tr>
<tr class="even">
<td>69</td>
<td>TFTP – UDP, Network Booting (PXE), Firmware updates, Config
Management</td>
</tr>
<tr class="odd">
<td>123</td>
<td>NTP – UDP, Synchronizes clocks across computer networks</td>
</tr>
</tbody>
</table>

<img src="./images/media/image11.png" style="width:2.22083in;height:0.83542in" />  
We have 3 choices for the domain. While the first two options look similar, if we append “http://” to the beginning, then we are using the full URL for the domain. The CNAME (Canonical name) is used as an alias to point one domain name to another name, such as pointing a sub-domain to a top-level domain. This leaves us with just the domain we’re looking for: **visual-networking.holidayhackchallenge.com.**

And we have 4 choices for the Request type:

<table>
<colgroup>
<col style="width: 8%" />
<col style="width: 91%" />
</colgroup>
<thead>
<tr class="header">
<th>A</th>
<th>Address Record, Maps a domain name to an IPv4 address</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>AAAA</td>
<td>Quad-A Record, Maps a domain name to an IPv6 address</td>
</tr>
<tr class="even">
<td>TXT</td>
<td>Text Record, Holds human-readable or machine-readable text data for
a domain</td>
</tr>
<tr class="odd">
<td>MX</td>
<td>Mail Exchanger Record, Directs email for a domain to the correct
mail servers</td>
</tr>
</tbody>
</table>

<img src="./images/media/image12.png" style="width:2.56319in;height:1.3125in" />
So, knowing this information, we can successfully choose the following options to complete this portion of the challenge.

<img src="./images/media/image13.png"
style="width:3.29861in;height:0.99097in" />

<img src="./images/media/image14.png" style="width:3.36181in;height:2.35486in" />
The next portion of the challenge is completing the TCP 3-Way handshake.

The TCP 3-way handshake is a process used to establish a reliable connection between a client and server, using three steps: SYN, SYN-ACK, and ACK. First, the client sends a SYN packet to the server to initiate the connection. The server responds with a SYN-ACK packet, acknowledging the client's request and sending its own synchronization sequence number. Finally, the client sends an ACK packet to confirm receipt of the server's response, and the connection is established for data transfer.

We have 6 choices for our TCP Flags:

<table>
<colgroup>
<col style="width: 8%" />
<col style="width: 91%" />
</colgroup>
<thead>
<tr class="header">
<th>URG</th>
<th>Urgent - Indicates that the data is urgent and should be processed
ahead of other data; uses an Urgent Pointer field</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>ACK</td>
<td>Acknowledgement - Confirms receipt of data packets; significant when
set</td>
</tr>
<tr class="even">
<td>PSH</td>
<td>Push - Tells the receiver to push data to the application layer
immediately, without waiting for the buffer to fill</td>
</tr>
<tr class="odd">
<td>RST</td>
<td>Reset - Abruptly terminates a connection, often due to an error or
unexpected packet</td>
</tr>
<tr class="even">
<td>SYN</td>
<td>Synchronize - Used to initiate a connection, synchronizing sequence
numbers between sender and receiver</td>
</tr>
<tr class="odd">
<td>FIN</td>
<td>Finish - Signals the graceful termination of a connection,
indicating no more data will be sent from that side</td>
</tr>
</tbody>
</table>

Before a client attempts to connect with a server, the server must first
bind to and listen at a port to open it up for connections: this is
called a passive open. Once the passive open is established, a client
may establish a connection by initiating an active open using the
three-way (or 3-step) handshake:

1.  **SYN**: The active open is performed by the client sending a SYN to
    the server. The client sets the segment's sequence number to a
    random value A.
<img src="./images/media/image15.png" style="width:3.66111in;height:2.55694in" />

2.  **SYN-ACK**: In response,
    the server replies with a SYN-ACK. The acknowledgment number is set
    to one more than the received sequence number i.e. A+1, and the
    sequence number that the server chooses for the packet is another
    random number, B.

3.  **ACK**: Finally, the client sends an ACK back to the server. The
    sequence number is set to the received acknowledgment value i.e.
    A+1, and the acknowledgment number is set to one more than the
    received sequence number i.e. B+1.

<img src="./images/media/image16.png" style="width:3.61667in;height:2.89028in" />
Steps 1 and 2 establish and acknowledge the sequence number for one direction (client to server). Steps 2 and 3 establish and acknowledge the sequence number for the other direction (server to client). Following the completion of these steps, both the client and server have received acknowledgments and a full-duplex communication is established.

Our third part of the challenge is to create an HTTP GET request. An HTTP GET request is a specific type of message sent by a client to a server to retrieve a specified resource, like a webpage, an image, or a piece of data (e.g., JSON or XML). It is the most common HTTP method and is fundamentally designed for safe, read-only operations that do not change the state of the server.

The 6 HTTP Verbs (Request types) that we are presented with are:

<table>
<colgroup>
<col style="width: 12%" />
<col style="width: 87%" />
</colgroup>
<thead>
<tr class="header">
<th>DELETE</th>
<th>Removes a specified resource from the server</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>GET</td>
<td>Requests data from a specified resource</td>
</tr>
<tr class="even">
<td>HEAD</td>
<td>Similar to GET, but only retrieves the headers, not the body, of a
resource</td>
</tr>
<tr class="odd">
<td>OPTIONS</td>
<td>Describes the communication options for the target resource</td>
</tr>
<tr class="even">
<td>POST</td>
<td>Sends data to a server to create or update a resource</td>
</tr>
<tr class="odd">
<td>PUT</td>
<td>Replaces the entire resource at a specific URL</td>
</tr>
</tbody>
</table>

We are also presented with 3 different HTTP Versions:

<table>
<colgroup>
<col style="width: 13%" />
<col style="width: 86%" />
</colgroup>
<thead>
<tr class="header">
<th>HTTP/1.0</th>
<th>One new TCP connection per request/response cycle, text based, High
latency</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>HTTP/1.1</td>
<td>Persistent TCP connections, added the HOST header, suffers from
Hold-of-line-blocking (HOLB) where one slow resource blocks others</td>
</tr>
<tr class="even">
<td>HTTP/2</td>
<td>Single TCP connection for multiple, parallel streams (multiplexing),
mandatory TLS encryption, request prioritization</td>
</tr>
</tbody>
</table>

We only have one option to select for the host, and the User-Agent is
left blank. We can fill in the User-Agent field by looking at our
Developer Tools in our browser and copying this information. This allows
mobile-optimized or desktop-optimized content to be sent accordingly, as
well as delivering specific code or layouts for different browser
version. For the purpose of this challenge, as long as we select “GET”
as our HTTP Verb, we will complete this portion. Changing the HTTP
Version will alter the response, and adding a User-Agent is reflected in
the challenge completion information.

Successfully completing this portion provides us with a redirect towards
HTTPS so that we can communicate securely.

<img src="./images/media/image17.png" style="width:3.10139in;height:3.11944in" />
The fourth part of this challenge is completing the TLS Handshake.

The goal of the TLS (Transport Layer Security) handshake is to set up a
secure connection so you can browse a website without anyone spying on
you or tampering with the data. To do this, your browser and the server
have to agree on three things:

1.  Encryption methods

2.  Identity (Proving the server is who they say they are)

3.  Session Keys (The actual password we will use for this conversation)

Here is the step-by-step breakdown:

The Core Concept: Asymmetric vs. Symmetric

<img src="./images/media/image18.png" style="width:2.32778in;height:2.96667in" />
Before looking at the steps, we need to understand the two types of keys used here:

-   Asymmetric Encryption (The Handshake): Used *only* at the start.
    There is a Public Key (everyone can see it, used to lock data) and a
    Private Key (only the server has it, used to unlock data). It's very
    secure but mathematically slow.

-   Symmetric Encryption (The Conversation): Used for the actual
    browsing. Both sides share the same key to lock and unlock data. It
    is incredibly fast.

The TLS Handshake is essentially using the slow, safe Asymmetric method
to agree on a key for the fast Symmetric method.

Step 1: The Negotiation (Client Hello)

Your browser (Client) connects to a website (Server) and sends a "Client
Hello."

-   "Here are the rules I know:" Your browser lists the encryption
    algorithms (Cipher Suites) it supports (e.g., "I can speak AES-256
    or ChaCha20").

-   "Here is a random number:" It sends a random string of data to be
    used later for math.

Step 2: The Agreement (Server Hello)

The Server picks the best encryption method from your list and replies.

-   "Let's use this one:" The server confirms which Cipher Suite you
    will both use.

-   "Here is my ID:" The server sends its SSL Certificate. This contains
    its Public Key and its digital signature.

-   "Here is my random number:" The server sends its own random string.

Step 3: Verification (The ID Check)

Your browser checks the Server's Certificate. It looks at the digital
signature to see if it was issued by a trusted authority (like DigiCert
or Let's Encrypt).

-   *If the check fails:* You get a big red warning screen ("Your
    connection is not private").

-   *If the check passes:* Your browser trusts that the Public Key in
    the certificate actually belongs to the website (e.g.,
    https://www.google.com/search?q=google.com) and not a hacker.

Step 4: The Key Exchange

Now your browser needs to send a secret to the server so they can build
a shared password.

-   Your browser creates a Pre-Master Secret.

-   It encrypts this secret using the server's Public Key (from the
    certificate).

-   It sends this encrypted secret to the server.

Because only the server has the Private Key, only the server can decrypt
this message. Now, both you and the server have the same secret, and no
one listening in knows what it is.

Step 5: The Session Keys

Now, both computers use that secret (plus the random numbers exchanged
earlier) to mathematically generate the Session Keys.

-   They switch from Asymmetric (Public/Private) to Symmetric (Shared
    Key) encryption.

-   They send a "Finished" message encrypted with this new key to prove
    it works.

<img src="./images/media/image19.png" style="width:2.57917in;height:2.76389in" />
Our final portion of this challenge is to complete the HTTPS GET request to retrieve the website
securely.

We have the same options as before, but we are now wanting to retrieve
the secure webpage after completing our TLS handshake. We can complete
this with any HTTP Version, however, choosing HTTP/2 provides a faster
and secure-by-design request.

<img src="./images/media/image20.png" style="width:3.18889in;height:0.78264in" />
Submitting our final HTTPS GET request gets us a successful completion for our first challenge of
HHC 25!

<img src="./images/media/image21.jpeg" style="width:2.80903in;height:1.15972in" />
If we continue south towards the Vendor Village, we meet Grace and Barry and our next challenges of
Spare Key and Storage Secrets.
