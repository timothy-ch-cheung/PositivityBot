import praw
import config
import time
import nltk
import re
from nltk.corpus import sentiwordnet as swn

SLEEP_TIME = 5


def botLogin():
    r = praw.Reddit(username=config.username, password=config.password, client_id=config.client_id,
                    client_secret=config.client_secret, user_agent="Positivity Rating Bot v1.0")
    return r


def getGif():
    return "https://media.giphy.com/media/1LweXxLwVT0J2/giphy.gif"


bot = botLogin()  # get instance of reddit with config.py

iterations = 1

wnl = nltk.stem.WordNetLemmatizer()

while True:
    print("iter_num:", iterations)
    for mention in bot.inbox.mentions(limit=25):  # comments where bot is mentioned
        comment = bot.comment(id=mention)
        parent_id = comment.parent_id

        if parent_id[:2] == "t3":  # a prefix of t3 is not a parent comment (its a submission)
            continue

        replied = False
        parent = bot.comment(id=parent_id[3:])  # remove prefix
        parent.refresh()  # parent comment object needs to be refreshed otherwise replies will be None

        # check if bot has already replied to this comment
        for reply in parent.replies:
            if reply.author.name == config.username:
                replied = True
                break

        if not replied and not parent.archived:
            parent_body = parent.body
            tagged_body = nltk.pos_tag(nltk.word_tokenize(parent_body))
            print(tagged_body)
            print(parent_body, "comment found")
            scores = []
            for word in tagged_body:
                word_lemma = wnl.lemmatize(word[0])  # lemmatize so sentiwordnet can recognise different wordforms
                breakdown = list(swn.senti_synsets(word_lemma))

                if len(breakdown) == 0:  # no word senses found
                    continue
                breakdown = breakdown[0]

                # (((pos - neg)*objectiveness)+1)/2
                scores.append((((breakdown.pos_score() - breakdown.neg_score()) * breakdown.obj_score()) + 1) / 2)

            score = sum(scores) / len(scores)  # mean valence of comment

            reply = "Positivity Rating:" + str(round(score, 2)) + " out of 1"

            if score < 0.5:  # Score lower than negativity threshold
                reply += "\n\n your comment was a bit negative, here's a gif to cheer you up! " + getGif()
            print(score)

            print("replying to comment")
            parent.reply(reply)

    print()
    iterations += 1
    time.sleep(SLEEP_TIME)
