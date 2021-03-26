#!/usr/bin/python
import requests
import time
import sys
from twython import Twython

# Get Settings from config file
import config

api = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS_KEY, config.ACCESS_SECRET)

lastPlayed = ""
tweeted = ""

# Call the playlist API, parse the currently playing song, form the tweet text.
def getPlaylist():
    URL = 'http://playlist.cprnetwork.org/api/playlistCO?n='+str(int(time.time()))
    r = requests.get(URL)
    oair = r.json()
    artist = addDateSpecific(oair[0]["artist"])
    tweet = oair[0]["start_time"].replace(" ", "") + " " + oair[0]["title"] + " by " + artist + " from " + oair[0]["album"]
    tweetu = tweet.decode('unicode-escape')
    tweetu = cap(tweetu, 277)
    return tweetu

# Post the tweet
def tweetLastPlayed(tweetText):
    curTime = str(time.strftime("%H:%M:%S"))
    print(curTime + " Tweeting: " + tweetText)
    api.update_status(status=tweetText)
    return

# Function to trim the tweet at a specified length & add elipsis
def cap(s, l):
    return s if len(s)<=l else s[0:l-3]+'...'

# Store the last tweet in a local file
def writeFile(log):
   lastTweetFile = open("/home/pi/python_scripts/I1023-playlist-v2/last_tweet.txt", "w")
   lastTweetFile.write(log)
   lastTweetFile.flush()
   lastTweetFile.close() 
   return

# Read the last tweet from the local file
def readFile():
    lastTweetFile = open("/home/pi/python_scripts/I1023-playlist-v2/last_tweet.txt", "r")
    lines = lastTweetFile.read()
    lastTweetFile.close()
    return lines

# Is it April Fool's Day? Add a joke. Ha ha.
def addDateSpecific(tText):
    if time.strftime("%B-%d") == "April-01":
        tText = tText + " & GWAR"
    return tText

# Get current song playing & compare to last tweet stored in the file.
# If different, tweet the current song & store the tweet in the local file.
def heavyLifting():
    tweeted = readFile()
    lastPlayed = getPlaylist()
    if tweeted != lastPlayed:
        tweetLastPlayed(lastPlayed)
        writeFile(lastPlayed)

# This is a hack, but it gets around the 1-minute granularity of cron
# by running the call four times and sleeping 15 seconds between each call
heavyLifting()
time.sleep(15)
heavyLifting()
time.sleep(15)
heavyLifting()
time.sleep(15)
heavyLifting()


