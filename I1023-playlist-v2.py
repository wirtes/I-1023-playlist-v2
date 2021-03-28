import coverpy
import requests
import tweepy
from datetime import datetime
import time
import sys
# Get Settings from local config file
import config
# Local Configurations
last_tweet_file_path = "/home/pi/python_scripts/I1023-playlist-v2/last_tweet.txt"

def post_tweet_and_art(tweet, cover_image):
    twitter_auth_keys = { 
        "consumer_key"        : config.CONSUMER_KEY,
        "consumer_secret"     : config.CONSUMER_SECRET,
        "access_token"        : config.ACCESS_KEY,
        "access_token_secret" : config.ACCESS_SECRET
    }

    auth = tweepy.OAuthHandler(
            twitter_auth_keys['consumer_key'],
            twitter_auth_keys['consumer_secret']
            )
    auth.set_access_token(
            twitter_auth_keys['access_token'],
            twitter_auth_keys['access_token_secret']
            )
    api = tweepy.API(auth)
    
    cur_time = str(time.strftime("%Y-%m-%d %H:%M:%S"))
    log_message = cur_time + " Tweeting: " + tweet
    
    if cover_image == "no_art":
        # No Artwork for this one. Post tweet without image
        post_result = api.update_status(status=tweet)
        log_message += " --no art found--"
    else:
        # Setup Twitter media upload
        media = api.media_upload(cover_image)
        # Post tweet with image
        post_result = api.update_status(status=tweet, media_ids=[media.media_id])
        
    print(log_message)
    
def download_art(band_and_album):
    c = coverpy.CoverPy()
    try:
        query = c.get_cover(band_and_album)
        response = requests.get(query.artwork())
        file = open(config.ALBUM_ART_TEMP_FILE, "wb")
        file.write(response.content)
        file.close()
        return True      
    except coverpy.exceptions.NoResultsException as e:
        #print("Nothing found.")
        return False

# Function to trim the tweet at a specified length & add elipsis
def cap(s, l):
    return s if len(s)<=l else s[0:l-3]+'...'

# Store the last tweet in a local file
def write_file(log):
    last_tweet_file = open(last_tweet_file_path, "w")
    last_tweet_file.write(log)
    last_tweet_file.flush()
    last_tweet_file.close() 
    return

# Read the last tweet from the local file
def read_file():
    last_tweet_file = open(last_tweet_file_path, "r")
    lines = last_tweet_file.read()
    last_tweet_file.close()
    return lines

# Is it April Fool's Day? Add a joke. Ha ha.
def easter_egg(tText):
    now = datetime.now()
    if now.strftime("%m-%d") == "04-01":
        tText = tText + " & GWAR"
    return tText

def get_current_song():
    # I'm hard coding this location because everything about this function is specific to this one radio station.
    URL = 'https://playlist.cprnetwork.org/won_plus3/KVOQ.json'
    r = requests.get(URL)
    now_playing = r.json()
    artist = easter_egg(now_playing[0]["artist"])
    title = now_playing[0]["title"]
    album = now_playing[0]["album"] 
    # Putting in a little hack because Indie 102.3 people only list the "album" as singles as "(Single)" sometimes.
    if album == "(Single)":
        album = now_playing[0]["title"] + " (Single)"
    # Format time exactly the way we like it
    start_time = datetime.strptime(now_playing[0]["time"], "%H:%M:%S")
    time = start_time.strftime("%-I:%M%P")
    # Compose the tweet text
    tweet_text = time + " " + title + " by " + artist + " from " + album
    tweet_text = cap(tweet_text, 277)
    # Use returned value for artist in case we changed the artist name on April Fools Day
    album_art_lookup_text = album + " " + now_playing[0]["artist"]
    
    return {"tweet_text": tweet_text, "album_art_lookup_text": album_art_lookup_text, "title": title}

def main():
    last_tweet = ""
    current_song = {}
    last_tweet = read_file()
    current_song = get_current_song()
    # Skips if: 
    #          1) We've already tweeted this song
    #          2) No song returned from API call.
    if last_tweet != current_song["tweet_text"] and len(current_song["title"]) > 0:
        write_file(current_song["tweet_text"])    
        if download_art(current_song["album_art_lookup_text"]):
            album_art_filename = config.ALBUM_ART_TEMP_FILE
        else:
            album_art_filename = "no_art"
        
        post_tweet_and_art(current_song['tweet_text'], album_art_filename)


# Hack to iterate multiple times per minute so that we can cron this script.
# Cron cannot run more frequently than once per minute.
number_of_checks_per_minute = 4
for i in range (0, number_of_checks_per_minute - 1):
    main()
    # Don't sleep after the last run
    if i < (number_of_checks_per_minute -1):
        time.sleep(60 / number_of_checks_per_minute)




