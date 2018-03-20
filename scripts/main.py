import praw
import spotipy
import os
import sys
import json
import config
import spotipy.util as util

def main():
    # Username input from terminal
    spotify_username = sys.argv[1]
    # Reddit object
    reddit = reddit_login()
    # Spotify object
    spotify = spotify_login(spotify_username)
    # Static Reddit subreddit variable
    sub_reddit_name = "music"
    # Music subreddit
    subreddit = reddit.subreddit(sub_reddit_name)

    # Iterate over reddit submissions and process spotify information
    for submission in subreddit.stream.submissions():
        processSubmission(submission, spotify)

def processSubmission(submission, spotify):
    # Split the submission title for info retrieval
    submission_title = submission.title.split("-")
    # Submission artist, the first item of the list above
    submission_artist = submission_title[0].strip()
    # Empty string
    songName = ""
    # None (NULL) value
    artistJson = None

    # If the list has a length of more than 1, then we probably have artist/song submission info
    if len(submission_title) > 1:
        songList = submission_title[1].split("[")
        songName = songList[0]

    # Search Request from Spotify on the artist
    searchRequest = spotify.search(submission_artist,1,0,"artist")
    #print(json.dumps(searchRequest, indent=4))

    # If we get a search reponse, get the artist name
    if searchRequest is not None:
        try:
            # Artist info
            artistJson = searchRequest['artists']['items'][0]
            artistName = artistJson['name']
            artistUrl = artistJson['external_urls']['spotify']

            # Query for search for
            songQuery = artistName + songName

            # Another request for the song
            songRequest = spotify.search(songQuery,1,0,"track")

            if songRequest is not None:
                # Let the try/catch handle the exception if no response
                song = songRequest['tracks']['items'][0]
                #print(json.dumps(songRequest, indent=4))

                songUrl = song['external_urls']['spotify']
                print("Replying to " + submission.title)
                submission.reply("Found it on Spotify! I think... i'm just a dumb bot " + songUrl)

        except:
            # swallow
            pass
            #print("Could not find artist!")

# Gets the Spotify user instance
def spotify_login(spotify_username):
    # Erase cache and prompt for user permission
    try:
        token = util.prompt_for_user_token(spotify_username)
    except:
        os.remove(f".cache-{spotify_username}")
        token = util.prompt_for_user_token(spotify_username)

    spotifyObject = spotipy.Spotify(auth=token)

    return spotifyObject

# Gets the Reddit bot instance
def reddit_login():
    redditObject = praw.Reddit(username = config.reddit_user,
                password = config.reddit_password,
                user_agent = config.reddit_user_agent,
                client_id = config.reddit_client_id,
                client_secret = config.reddit_client_secret)

    return redditObject

if __name__ == '__main__':
    main()
