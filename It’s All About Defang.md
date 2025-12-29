# It’s All About Defang
<img src="./images/media/image70.png" />
<img src="./images/media/image71.jpeg" />

From here, we’ll head over to City Hall and talk with Ed Skoudis.

We find out from Ed that there’s a new SOC tool being used to triage phishing emails, but it needs some refinement.  
<img src="./images/media/image72.jpeg" />

We click on the terminal and are brought up with a webpage for the Dosis Neighborhood SOC. We have a phishing email that we need to analyze and then build some rules around to help protect the users of the email network from future phishing attempts.

<img src="./images/media/image73.png"/>

First, we need to extract out the IOCs (Indicators of Compromise) and extract all suspicious domains, IPs, URLs, and email addresses.

We need to write one rule which will pull out all domains while not generating false positives, such as files or known good addresses. We can find three possibly malicious domains using the following domain pattern.

<img src="./images/media/image74.png"/>

<span class="mark">\b(?!.\*\\exe\b)(?\![A-Za-z0-9-\]\*dosisneighborhood)(?:(?!\d)(?!-)\[A-Za-z0-9-\]{1,63}(?&lt;!-)\\)+(?:\[A-Za-z\]{2,63})\b</span>

Next, we’ll look at IP addresses. Again, we need to avoid false positives such as phone numbers and times, so we can use the following IP Address Pattern to isolate only IP Addresses, of which we are able to grab two.

<span class="mark">\d{1,3}\\\d{1,3}\\\d{1,3}\\\d{1,3}</span>

<img src="./images/media/image75.png"/>

Next, we’ll look at URLs. We need to again make sure that we don’t generate any false positives or miss anything pertinent, so we can use the following pattern to isolate URLs, of which there are 2.

<img src="./images/media/image76.png" />
<span class="mark">https://\[a-zA-Z0-9-\]+(\\\[a-zA-Z0-9-\]+)+(:\[0-9\]+)?(/\[^\s\]\*)?</span>

Finally, we’ll look at email addresses. We want to make sure we are only getting email addresses with this and not URLs or domains. We can use the following pattern and retrieve two emaill addresses.

<img src="./images/media/image77.png"/>
<span class="mark">\b\[a-zA-Z0-9.\_%+-\]+@\[a-zA-Z0-9.-\]+\\\[a-zA-Z\]{2,}\b</span>

<img src="./images/media/image78.png"/>
Next, we need to move on to generating our report. We need to check any of our results for non-malicious items, remove them if necessary, and then move on to step 2, Defanging and submitting our report.  
  
Defanging consists of removing all items from the malicious results which might allow an accidental click to activate a link or file. This includes replacing dots/periods with \[.\] and @ with \[@\] and http with hxxp and :// with \[://\]. We can use the following SED rule to defang all of our items before submitting

<span class="mark">s/\\/\[.\]/g; s/@/\[@\]/g; s/http/hxxp/g; s/:\\/\[://\]/g</span>
