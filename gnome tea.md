# Gnome Tea

<img src="./images/media/image176.png"/>

<img src="./images/media/image177.png" />

First upon starting the challenge, we are presented with a login page for GnomeTea. We don't have a login and the only way to get one is to contact the gnome admin, which isn't going to happen… Just for kicks, let's see what happens whenever we try to log in with random creds:  

<img src="./images/media/image178.png"/>

That of course didn't log us in, but we now know that this is running Firebase. Now, there are several different Firebase based vulnerabilities. I first tried this one: <https://www.clear-gate.com/blog/firebase-authentication-misconfiguration/> however it's locked down.  
  
I then checked out this super informative talk at <https://isc.sans.edu/diary/32158> but didn't find a way to make use of the exploits shown. I then dove back into the source code to see what might be helpful there. Using BurpSuite, I found /assets/index-BVLyJWJ\_.js which provided some interesting information.

This appears to be the main application bundle for a React Single Page Application (SPA) which uses Firebase for its backend.

-   **Frontend Framework:** React 18.3.1

-   **Routing:** React Router DOM v6.30.1

-   **Backend/BaaS:** Firebase v11.10.0 (Auth, Firestore)

-   **Build Tool:** Likely Vite (based on the file naming convention and
    structure).

The code contains hardcoded Firebase configuration details. While this is standard for Firebase web apps, it allows us to interact with the backend directly.

-   **Project ID:** holidayhack2025

-   **Auth Domain:** holidayhack2025.firebaseapp.com

-   **API Key:** AIzaSyDvBE5-77eZO8T18EiJ\_MwGAYo5j2bqhbk

-   **Messaging Sender ID:** 341227752777

-   **App ID:** 1:341227752777:web:7b9017d3d2d83ccf481e98

**3. Routing Structure**

The application defines several routes managed by the zP function in the code:

<table>
<colgroup>
<col style="width: 23%" />
<col style="width: 16%" />
<col style="width: 59%" />
</colgroup>
<thead>
<tr class="header">
<th>Route</th>
<th>Component</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>/login</td>
<td>VP</td>
<td>The entry point/login screen.</td>
</tr>
<tr class="even">
<td>/dashboard</td>
<td>LP</td>
<td>The main landing page after login.</td>
</tr>
<tr class="odd">
<td>/gnome/:gnomeId</td>
<td>MP</td>
<td>A profile viewer for specific "Gnomes".</td>
</tr>
<tr class="even">
<td>/tea</td>
<td>FP</td>
<td>A feed of gossip/posts ("Tea Feed").</td>
</tr>
<tr class="odd">
<td>/messages</td>
<td>UP</td>
<td>Direct messages functionality.</td>
</tr>
<tr class="even">
<td>/admin</td>
<td>jP</td>
<td>An operations dashboard. (This is ultimately where we want to end
up!!)</td>
</tr>
<tr class="odd">
<td>/</td>
<td>Pv</td>
<td>Redirects to /login.</td>
</tr>
</tbody>
</table>

<img src="./images/media/image179.png"/>

Now we're cooking with fire! The first thing to do is see if we can dump any information as an anonymous user. We can attempt to do this manually, but let's instead create a script with the information we have and see if we can dump everything:

<img src="./images/media/image180.png" />
<img src="./images/media/image181.png"/>

If we do a simple grep command to search recursively for "password" we see that we have a few good things to check for.

Looks like have a message that says Barnaby wrote a password down on a post it!! Now, we need his email address. Let's do another grep for emails.

Okay, that's awesome! We now have everyone's email address and a possible password for Barnaby.

`barnabybriefcase@gnomemail.dosis:MakeRColdOutside123!`

If we try to log in with these creds, it looks like it’s a red herring… If we look at those messages again, we also see that he tells Glitch that his password is actually the name of his hometown. Let's see if we can find out what his hometown is!

If we open up the gnomes\_dmp.json that we created, we find the entry for Barnaby and it includes some images. 

<img src="./images/media/image182.png" />

His Profile Avatar:  

<img src="./images/media/image184.png" />

And his Driver's license:

<img src="./images/media/image183.png" />

Bummer!! Looks like this is locked down. Just for kicks, let's see if we can pull any of the other licenses and avatars. We can generate a list of URLs to download from for both Avatars and Licenses from the dump info we got and then script out a downloader for each:

<img src="./images/media/image185.png"/>

<img src="./images/media/image186.png" /> 

Hmm… Looks like we get an error on the same one as earlier for Barnaby, but we are able to download all of the others as well as the avatars.

<img src="./images/media/image187.png" />

<img src="./images/media/image188.png" /> 

We need to see if there's a way to download the files as an authenticated user instead of anonymously. We found the hardcoded Admin UID earlier, so let's see if we can craft a script with that and download it!

<img src="./images/media/image190.png"/>

This looks promising, we have 18 avatars and 18 licenses downloaded. Let's see if we can open up Barnaby's license!!

<img src="./images/media/image189.jpeg"/>

Now, this has his address on it, but not his hometown… He mentioned taking his picture there, so let's see if there's anything hiding inside the exif data of this image. We can use the tool exiftool to examine all of the exif data by using `exiftool gnome-documents\_l7VS01K9GKV5ir5S8suDcwOFEpp2-drivers\_license.jpeg`

<img src="./images/media/image191.png" />

We have some GPS coordinates! Let's take a look at where these come back to:

<img src="./images/media/image192.png" />

Looks like Barnaby comes from Gnomesville! If we take that back to the login page, we see that we can finally authenticate into the app as Barnaby!!

<img src="./images/media/image194.png"/>
<img src="./images/media/image195.png" />
<img src="./images/media/image193.png"/>

Now, if we go into the console, we can see if we can pass the Admin UID from earlier to elevate our privileges…

And bingo!! We have successfully logged in as Barnaby and elevated our privileges and found out the secret phrase!!

Okay, that was a fun step up into Act III! Now, let’s head over to the Data Center and speak with Chris Davis.
