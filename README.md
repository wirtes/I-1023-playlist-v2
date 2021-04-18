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

updated.
