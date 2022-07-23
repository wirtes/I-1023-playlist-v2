# I-1023-playlist-v2
Script to determine the current song playing on Colorado radio station Indie 102.3 and tweet to @oaplaylist account.

**This is completely unoffical and in no way sanctioned by Colorado Public Radio or Indie 102.3. I'm just piggybacking on their webpage APIs.** (I hope they don't mind.) They're a good station full of great people. So you should listen to them here: https://www.cpr.org/indie/

This script will poll the playlist API for radio station Indie 102.3 in Colorado, https://www.cpr.org/indie/ every 15 seconds to get the latest song playing. 

When the song changes, it will tweet it the Twitter account @oaplaylist, https://twitter.com/oaplaylist

## Configuration
Rename "config_sample.py" to "config.py" and add your Twitter account information to post to your Twitter account. Also specify the location on your server for some working files.

## Running the script

Setup a cron job to run the script every minute. Configure the script for how many times per minute it should check the API.

## Requirements
This script is written for Python 3.x. 

It relies on the following modules: coverpy, requests, tweepy, datetime, time, sys, pillow.

## April Fools' Day Easter Egg
This script also checks to see if the date is 1-Apr, and it gives a hook to modify the tweet accordingly. Currently, it adds the text " & GWAR" to the band name and superimposes and image of GWAR on top of the album cover. Some people find this humorous. Samples can be found here: https://twitter.com/search?q=from%3Aoaplaylist%20since%3A2021-04-01%20until%3A2021-04-02&src=typed_query&f=live

![gogos](https://user-images.githubusercontent.com/11652957/134274102-d402207e-e924-48de-9905-81c049cf9f17.png)

![beastie_boys_and_GWAR](https://user-images.githubusercontent.com/11652957/180614683-923f5af7-8d1d-4ed1-8204-47c815b6b50f.png)

![immunity](https://user-images.githubusercontent.com/11652957/134274134-855a803d-0b7e-40b5-90ef-302660feb6bb.png)
