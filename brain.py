import tweepy
import getpass
import markov
import reddit
import time
import logging

username = raw_input("Username: ")
password = getpass.getpass("Password: ")

auth = tweepy.BasicAuthHandler(username, password)
identica = tweepy.API(auth_handler=auth, host='identi.ca', api_root='/api')
_STATUS_CHAR_LIMIT = 140

reddit_ = reddit.Reddit()
place_holder = None
#_WAIT_TIME = 30 * 60 # 30 minutes * 60 seconds
_WAIT_TIME = 30
# Max comments to fetch each iteration
_MAX_COMMENTS = 500

markov_ = markov.MarkovChain()
_MAX_TOKENS = 40

while True:
    try:
        new_comments = reddit_.get_comments(limit=_MAX_COMMENTS,
                                            place_holder=place_holder)
        for comment in new_comments:
            markov_.add(comment.body.split(" "))

        new_chain = markov_.random_output(max=_MAX_TOKENS)
        status = " ".join(new_chain)
        status = status[:_STATUS_CHAR_LIMIT]

        identica.update_status(status)

        time.sleep(_WAIT_TIME)
    except Exception:
        continue

