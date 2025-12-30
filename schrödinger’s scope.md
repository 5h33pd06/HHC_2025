# Schrödinger’s Scope

<img src="./images/media/image222.png"/>

When we click on the terminal for this challenge, we are taken to a website to perform a penetration test against the `/register` endpoint.

<img src="./images/media/image227.png" />
<img src="./images/media/image226.png" />
<img src="./images/media/image228.png" />

Now, if we’re not quick, we will start to see that we send out of scope requests almost immediately.

<img src="./images/media/image225.png" />

If we want to have full control over this test and not send anything out of scope, we need to start this challenge up in BurpSuite and start capturing requests so that we can remove the offending request. The first thing we can do is set BurpSuite to drop all out of scope requests and make sure that /gnomeU is set to be out of scope. We will need to be very cautious as we move through as well because the gnomes appear to be helpful, but often are trying to get us to go out of scope!

Once we have some initial items set to be in and out of scope, we can restart the challenge and see if we can get a 100%!

<img src="./images/media/image229.png"/>

Now, once we start, we can click on “Enter Registration System” which takes us to the “Student Login” page. We also see that our web address has gone to the /register endpoint. The gnome on this page does give us a hint of using a sitemap, so let’s see if /register/sitemap exists…

<img src="./images/media/image231.png"/>

Looks like this gets us a pretty full sitemap to work with! Now, we want to make sure that we don’t visit anything outside of the /register endpoint, but we also shouldn’t take this listing to be the complete listing either. Developers can often get lazy or predictable and reuse endpoints in various areas, so we should look at all of the endpoints and see if any of them have been carried over into the new /register endpoint. We do see that there are /wip/register, /wip/register/dev, /wip/register/dev/dev\_notes, and /wip/register/dev/dev\_todos that might be interesting if they have been carried over to the new /register endpoint! 

<img src="./images/media/image230.png"/>

The only one that gives us anything useful so far is /register/dev/dev\_todos, which also gets us our 1<sup>st</sup> finding for our report! We can take those creds to the login page and try to log in, however we get an error.

<img src="./images/media/image232.png" />

Looks like we will need to use Burp to edit our request and make sure to include `X-Forwarded-For: 127.0.0.1` within the header of our requests going forward.

Once we do that, we are able to get logged in, and we score our 2<sup>nd</sup> vulnerability on our report! Now that we have authorization, let’s go back and see if we can hit those other dev endpoints.

<img src="./images/media/image233.png" />

<img src="./images/media/image234.png" />

<img src="./images/media/image235.png"/>

<img src="./images/media/image236.png"/>

Okay, so we have some traction! We’re given a course name and that it is in “wip” phase, so we can use this info later. We can use some of the other endpoints we found in the sitemap and we see that in /register/courses there is a commented note pointing to /register/courses/search. We can find an endpoint /register/courseSearchUnlocked inside the registerCourses.js file. If we send a POST request here, we should be able to open up the /register/courses/search endpoint.

Now that we have access to the search system (and our 3<sup>rd</sup> vulnerability), we can see about searching for courses.

<img src="./images/media/image237.png" />

Since we have a search field, let’s check for SQLi. Awesome! We find our 4<sup>th</sup> vulnerability, and if we scroll down, we see GNOME 827. If we click on that, we are given the option to “Report | Remove Course | Continue”. We can click on Report and we get our 5<sup>th</sup> vulnerability.

<img src="./images/media/image242.png" />

Now, we have one more vulnerability to go… We had a dev\_note telling us about the holiday\_behavior course, but we haven’t found it yet. Let’s see if we can find that. We can try navigating to /register/courses/wip/holiday\_behavior, but it tells us we don’t have permission due to an invalid session registration value. 

<img src="./images/media/image243.png"/>

Let’s check in with Burp Intruder and see if we can fuzz that value.

<img src="./images/media/image244.png"/>

We can setup our attack by choosing the last two values of the registration cookie. To make it easy, setup both value as its own position, then do a Cluster bomb attack with each payload list being the characters a-f0-9 to iterate through all of the hex values.

<img src="./images/media/image245.png"/>

When we run the attack, we find a value that returns a status code 200 and shows us the WIP course!

Now, if we go back to our regular Burp Proxy window, we can intercept the request and then refresh the browser window. Once we do that, we can put our valid registration value in and forward the page and that shows us that we’ve found all of the vulnerabilities!

And once we click Finalize Test, we see that we have successfully completed everything, and we stayed completely within the scope of the assessment!

<img src="./images/media/image246.png" />

That was quite the chore! This was a great reminder to always maintain the scope whenever performing a pentest, even whenever there are interesting things that might be vulnerable! There were plenty of opportunities, both in and out of our direct control, to go out of scope, so it’s important to know how to use our tools to maintain accountability and know what the system is doing.

<img src="./images/media/image247.png"/>

Let’s move on to our next challenge and head to the Grand Hotel and talk with Tom.
