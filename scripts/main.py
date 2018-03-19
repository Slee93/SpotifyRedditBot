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
    for submission in subreddit.submissions():
        processSubmission(submission, spotify)

def processSubmission(submission, spotify):
    # Split the submission title for info retrieval
    submission_title = submission.title.split("-")
    # Submission artist, the first item of the list above
    submission_artist = submission_title[0].strip()
    # Empty string
    song = ""
    # None (NULL) value
    artist = None

    # If the list has a length of more than 1, then we probably have artist/song submission info
    if len(submission_title) > 1:
        song = submission_title[1].strip()

    # Search Request from Spotify on the artist
    searchRequest = spotify.search(submission_artist,1,0,"artist")
    #print(json.dumps(searchRequest, indent=4))

    # If we get a search reponse, get the artist name
    if searchRequest is not None:
        try:
            # Artist info
            artist = searchRequest['artists']['items'][0]
        except:
            # swallow
            pass
            #print("Could not find artist!")

    if artist:
        popularity = artist['popularity']
        print(artist['name'] + " : " + str(popularity))

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
