import praw
import spotipy
import os
import config
import spotipy.util as util

def main():
    reddit = reddit_login()
    spotify = spotify_login()

    subreddit = reddit.subreddit("Music")

    for submission in subreddit.submissions():
        processSubmission(submission)

def processSubmission(submission):
    submission_title = submission.title.split("-")
    artist = submission_title[0].strip()
    song = ""

    if len(submission_title) > 1:
        song = submission_title[1].strip()

    print(artist + ": " + song)

def spotify_login():
    token = util.prompt_for_user_token(config.spotify_user)

    spotifyObject = spotipy.Spotify(auth=token)

    return spotifyObject

def reddit_login():
    redditObject = praw.Reddit(username = config.reddit_user,
                password = config.reddit_password,
                user_agent = config.reddit_user_agent,
                client_id = config.reddit_client_id,
                client_secret = config.reddit_client_secret)

    return redditObject

if __name__ == '__main__':
    main()
