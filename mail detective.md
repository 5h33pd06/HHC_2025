# Mail Detective

<img src="./images/media/image127.png" />

<img src="./images/media/image128.png"/>

For our next challenge, we are presented with another terminal which allows us to investigate the IMAP server using the CLI.

<img src="./images/media/image129.png" />

We are provided with the TCP port 143 and the backdoor credentials into the system: `dosismail:holidaymagic`

Now, at this point, if we’re not familiar with using curl commands to investigate IMAP, then we can use some commands to get us started. `curl --help all` will show us all of the options available to us. We have the credentials we need to access the server, so using `curl --help auth` and `curl --help imap` will provide the rest of the commands we need to get us through this challenge.

<img src="./images/media/image130.png"/>

After looking through the commands available to us, we see that we can start enumerating the server with `curl -u dosismail:holidaymagic imap://localhost:143/`

That output confirms that the INBOX folder exists, but it doesn't show us the emails inside it yet. In IMAP, listing a folder usually just returns its attributes (like \HasNoChildren).

To actually see the emails, we need to search the folder for messages and then **fetch** them.

<img src="./images/media/image131.png" />

These numbers (1, 2, 3) are the IDs of the emails. Once we have an ID, we can download the content of that specific email by appending ;UID=1 to the folder path.

Just to be thorough, let's check the other directories:

<img src="./images/media/image132.png"/>

Looks like there are other messages outside of the INBOX as well

<img src="./images/media/image133.png" />

We know we need to look for an email containing a pastebin link, so let's search for that keyword. Looks like only the Spam folder has an email with that, so that's most likely our malicious email!

<img src="./images/media/image134.png"/>

<img src="./images/media/image135.png"/>

There's our pastebin link!

Now, for kicks, we can also use the commands we’ve learned to look through all of the emails and see what’s there. There are some interesting emails, but nothing else that pertains to our challenge, so I’ll leave that for your own interest later.

After investigating IMAP, I’m a little hungry, so let’s head on over to Sasabune for some sushi and our next challenge!
