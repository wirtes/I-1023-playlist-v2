#!/usr/bin/python
import requests
import time
import sys
from twython import Twython

# Get Settings from config file
import config.py


api = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS_KEY, config.ACCESS_SECRET) 

lastPlayed = ""
tweeted = ""

def getPlaylist():
    URL = 'http://playlist.cprnetwork.org/api/playlistCO?n='+str(int(time.time()))
    r = requests.get(URL)
    oair = r.json()
    artist = addDateSpecific(oair[0]["artist"])
    tweet = oair[0]["start_time"].replace(" ", "") + " " + oair[0]["title"] + " by " + artist + " from " + oair[0]["album"]
    tweetu = tweet.decode('unicode-escape')
    tweetu = cap(tweetu, 277)
    return tweetu
    
def tweetLastPlayed(tweetText):
    curTime = str(time.strftime("%H:%M:%S"))
    print(curTime + " Tweeting: " + tweetText)
    api.update_status(status=tweetText)
    return

def cap(s, l):
    return s if len(s)<=l else s[0:l-3]+'...'
    
def writeFile(log):
   lastTweetFile = open("/home/pi/python_scripts/I1023-playlist-v2/last_tweet.txt", "w")
   lastTweetFile.write(log)
   lastTweetFile.flush()
   lastTweetFile.close() 
   return

def readFile():
    lastTweetFile = open("/home/pi/python_scripts/I1023-playlist-v2/last_tweet.txt", "r")
    lines = lastTweetFile.read()
    lastTweetFile.close()
    return lines
    
def addDateSpecific(tText):
    if time.strftime("%B-%d") == "April-01":
        tText = tText + " & GWAR"
    return tText
    
def heavyLifting():
    tweeted = readFile()
    lastPlayed = getPlaylist()
    if tweeted != lastPlayed:
        tweetLastPlayed(lastPlayed)  
        writeFile(lastPlayed)        


heavyLifting()
time.sleep(15)
heavyLifting()
time.sleep(15)
heavyLifting()
time.sleep(15)
heavyLifting()


