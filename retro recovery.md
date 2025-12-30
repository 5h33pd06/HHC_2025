# Retro Recovery

<img src="./images/media/image108.png" />

<img src="./images/media/image109.png"/>
<img src="./images/media/image110.png"/>

We head over to the Retro Arcade and we talk with Mark DeVito. While here, we also pick up the floppy disk item.

We can analyze this in any number of programs, but I chose to look at it in the free program FTK Imager. This program allows for an image of a disk to be loaded and quickly triaged to look for files.

First we will add the image to our “case"

<img src="./images/media/image111.png" /><img src="./images/media/image112.png"/>

<img src="./images/media/image113.png" />

And then we have the ability to explore through the filesystem of the disk and see what we can find!

We are first presented with the root directory and unallocated space. Unallocated space can often show some interesting artifacts such as
deleted files!

<img src="./images/media/image114.png" />

We’ll first look at the root directory, which contains the directory “qb45” and two deleted files “.all\_i-want\_f” and “all\_i-want\_for\_christmas.bas”. We see that “.all\_i-want\_f” just appears to be a pointer file to “all\_i-want\_for\_christmas.bas”, so that’s where we should look next.

<img src="./images/media/image115.png"/>

Now this is a little more exciting! We can see that this is a program written in BASIC and appears to be a modified version of the classic Star Trek game!! (One of my favorite classic BASIC games!! I spent SOOOO much time playing this as a kid. This was one of the first programs that I modded myself in an attempt to add some of the other alien races encountered in TNG.)

A quick perusal through the beginning of the file shows something interesting! We get to line 211 and find a string of what appears to be b64 encoded text!! We haven’t seen any other b64 encoded text in this program yet, so let’s see what this shows us!

<img src="./images/media/image116.png" />

We can pop that code into trusty CyberChef and decode it to get our flag!

<img src="./images/media/image117.png" />

That successfully completes the challenge. Now, I’m curious, as I haven’t played this game in years, but can I actually export this and play it??

We can right click on the file and go to “Export Files…”

<img src="./images/media/image118.png"/>

And then using DOSBox, we can actually load this program up and play it in all of its black and white, text-based glory!!!

<img src="./images/media/image119.png" />
<img src="./images/media/image120.png" />

At this point in the HHC I might have gotten a little derailed on the mission and spent some time playing this game for old time’s sake…

After playing several rounds of Super Star Trek, it’s time to jump back in to the HHC and move on to our next challenge.

Let’s go ahead and talk with Kevin while we’re here and see what he’s got for us!
