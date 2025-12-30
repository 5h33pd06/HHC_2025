# IDORable Bistro

<img src="./images/media/image136.png" />

<img src="./images/media/image137.jpeg" />
<img src="./images/media/image138.jpeg"/>
<img src="./images/media/image139.png"/>

As we head over to Sasabune, we see that there’s a crumpled receipt laying outside on the sidewalk.

<img src="./images/media/image140.png" />

While not typically a wise security move to just go around scanning random QR codes we find, let’s scan this one and see if it helps us with anything for this challenge.

I used <https://qrcoderaptor.com> to decode this QR and received the URL <https://its-idorable.holidayhackchallenge.com/receipt/i9j0k1l2>. If we go to that website, we see that we get a full breakdown of the receipt.

Now, any time I see something like the Receipt \# in the URL, I think that this is possibly vulnerable to IDOR. This is obfuscated initially by the "i9j0k1l2" string, and it's probably possible to run Burp Intruder long enough to search through all 200+million possibilities (I initially tried this while I was doing further recon and Burp couldn't handle it inside my VM…) Going back to the KISS principal, I decided to do some more digging in the browser, and we can check developer tools and get the API call.

<img src="./images/media/image141.png" /> 
<img src="./images/media/image142.png" />

Now, this looks a bit more promising! This shows us our exact receipt number and is going to be much easier to enumerate. We can do this manually, however there are other ways of doing this, such as creating a custom script or using a fuzzer. I decided to use Burp Intruder to do this

<img src="./images/media/image143.png" />

I loaded the API call into Intruder and selected the ID field as the position I wanted to fuzz.

Next, I used the "Payload type" field to select "Numbers" and then chose a sequential number range from 0 to 200 with a step of 1. 201 requests is MUCH better than 200+ million!!

<img src="./images/media/image144.png" />

If we look for all of the results with a status code of 200, then we can see all of the valid receipts. Looking through the receipts, we see receipt 139 for Bartholomew Quibblefrost, so there's our Gnome!

After a nice bite to eat, let’s head on over to the 24-Seven to pick up some snacks and gamer-fuel to keep us going on our marathon hacking session to push through to save Christmas!
