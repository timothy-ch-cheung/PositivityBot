import praw
import config
import time
import random

sleep = 5

activeMode = False

subreddit_name = "test"
thread_url = "https://www.reddit.com/r/test/comments/7e02x7/brumhack_70/"
#thread_url = "https://www.reddit.com/r/test/comments/7e00jv/test2/"

file = open("wordList.txt", "r")
wordList = file.read()
wordList = wordList.split("\n")
word_list = []

file = open("links.txt", "r")
links = file.read()
links = links.split("\n")
file.close()

for word_rating in wordList:
    word_rating = word_rating.split(",")
    word_list.append([word_rating[0], word_rating[1]])

def BMP(s):
    return "".join((i if ord(i) < 10000 else '\ufffd' for i in s))

##def containsReply(comment): #doesn't work
##    reply = True
##    replies = comment.replies
##    print(replies)
##    for reply in replies:
##        print(reply.body)
##        if "this was posted by positivityRatingBot" in reply.body:
##            reply = False
##            
##    return reply

def getSavedComments ():
    file = open("replied_comments.txt", "r")
    replied_comments = file.read()
    output = replied_comments.split("\n")
    file.close()
    return output

def saveComments():
    file = open("replied_comments.txt", "w")
    output = ""
    for comment in replied_comments:
        output += comment + "\n"
    output = output[:len(output)-1]
    file.write(output)
    file.close()

def botLogin():
    r = praw.Reddit(username = config.username,password = config.password,client_id = config.client_id, client_secret = config.client_secret,user_agent = "testing bot")
    return r

def gradeComment(comment):
    rating = 0
    words = 0
    comment = comment.lower().replace("[^A-Za-z]"," ").split(" ")
    for i in range (len(word_list)):
        if word_list[i][0] in comment:
            rating += float(word_list[i][1])
            if int(float(word_list[i][1])) == 1:
                words += 2
            else:
                words += 1
    
    if rating == 0 or words == 0:
        return 1
    else:
        rating = rating/words
        if rating < 1:
            return 1
        else:
            return 1/rating

def runBot(r, mode):
    posts = 0
    if mode == "thread":
        comment_forest = r.submission(url = thread_url).comments
        comments = comment_forest.list()
        for comment in  comments:   #run in specific thread
            if "this was posted by positivityRatingBot" not in comment.body and comment.id not in replied_comments:
                if comment.body == "Summon u/positivityRatingBot":
                    parent = comment.parent()
                    grade = gradeComment(BMP(parent.body))
                    comment.reply("this bot thought your positivity rating of your comment is " + str(grade) + "\n\n (this was posted by positivityRatingBot)  \n\n 0 = negative, 1 = positive" )
                    replied_comments.append(comment.id)
                    print("rating: " , grade)
                    posts += 1
                    print("MADE A SUMMON POST")
                else:
                    grade = gradeComment(BMP(comment.body))
                    print("rating: " , grade)
                    print(BMP(comment.body))
                    if grade < 0.3 and activeMode:
                        random.shuffle(links)
                        comment.reply("You seem a bit down, maybe this will cheer you up: [Here](" + links[0] +")" "\n\n (this was posted by positivityRatingBot - summon this bot by replying 'Summon u/positivityRatingBot' to the post you want to analyze) \n\n your positivity rating is " + str(grade) + "  \n\n 0 = negative, 1 = positive")
                        replied_comments.append(comment.id)
                        posts += 1
                        print("MADE A POST")
                    print("______________________________________________________________________________________________________________________________________________________________")
            else:
                print("skipped:")
                print(BMP(comment.body))
                print("______________________________________________________________________________________________________________________________________________________________")
    if mode == "subreddit":
        for comment in r.subreddit(subreddit_name).comments(limit = 50) :   #run in specific subreddit
            if "this was posted by positivityRatingBot" not in comment.body and comment.id not in replied_comments:
                if comment.body == "Summon u/positivityRatingBot":
                    parent = comment.parent()
                    grade = gradeComment(BMP(parent.body))
                    comment.reply("this bot thought your positivity rating of your comment is " + str(grade) + "\n\n (this was posted by positivityRatingBot)  \n\n 0 = negative, 1 = positive" )
                    replied_comments.append(comment.id)
                    print("rating: " , grade)
                    posts += 1
                    print("MADE A SUMMON POST")
                else:
                    grade = gradeComment(BMP(comment.body))
                    print("rating: " , grade)
                    print(BMP(comment.body))
                    if grade < 0.3 and activeMode:
                        random.shuffle(links)
                        comment.reply("You seem a bit down, maybe this will cheer you up: [Here](" + links[0] +")" "\n\n (this was posted by positivityRatingBot - summon this bot by replying 'Summon u/positivityRatingBot' to the post you want to analyze) \n\n your positivity rating is " + str(grade) + "  \n\n 0 = negative, 1 = positive")
                        replied_comments.append(comment.id)
                        posts += 1
                        print("MADE A POST")
                    print("______________________________________________________________________________________________________________________________________________________________")
            else:
                print("skipped:")
                print(BMP(comment.body))
                print("______________________________________________________________________________________________________________________________________________________________")

    saveComments()
    print("made " + str(posts) + " posts  ...sleeping")
    time.sleep(sleep)
    
replied_comments = getSavedComments()
mealdeal = botLogin()

userMode = input("enter mode (T = thread, S = subreddit)\n(add * to override default subreddit/thread url)\n(end mode with $ to switch to active mode) e.g. T*$ \n")


if userMode[:2] == "T*":
    mode = "thread"
    thread_url = input("input thread url:\n ")
elif userMode[:2] == "S*":
    mode = "subreddit"
    subreddit_name = input("input subreddit:\n ")
elif userMode[:1] == "S":
    mode = "subreddit"
elif userMode[:1] == "T":
    mode = "thread"
else:
    print("invalid mode")

if userMode[-1] == "$":
    activeMode = True

while True:
    runBot(mealdeal, mode)
    replied_comments = getSavedComments()

#runBot(mealdeal, mode)

##while True:
##    try:
##        runBot(mealdeal)
##        replied_comments = getSavedComments()
##    except:
##        print("post limit reached")
