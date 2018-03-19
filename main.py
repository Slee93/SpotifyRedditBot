import praw
import config

def main():
    reddit = praw.Reddit(username = config.reddit_user,
                        password = config.reddit_password,
                        user_agent = config.reddit_user_agent,
                        client_id = config.reddit_client_id,
                        client_secret = config.reddit_client_secret)


if __name__ == '__main__':
    main()
