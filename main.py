import praw
import config

def main():
    reddit = praw.Reddit(username = config.reddit_user,
                        password = config.reddit_password,
                        user_agent = config.reddit_user_agent,
                        client_id = config.reddit_client_id,
                        client_secret = config.reddit_client_secret)

    subreddit = reddit.subreddit("Music")
    for submission in subreddit.submissions():
        processSubmission(submission)

def processSubmission(submission):
    submission_title = submission.title.split("-")
    artist = submission_title[0].strip()
    song = ""
    
    if len(submission_title) > 1:
        song = submission.title.split("-")[1].strip()

    #print(artist)
    print(song)

if __name__ == '__main__':
    main()
