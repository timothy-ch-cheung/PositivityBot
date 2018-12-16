file = open("words.txt", "r")
wordList = file.read()
file.close()
wordList.split("\n")
output_list = []

for word_rating in wordList:
    word_rating.split(",")
    word = word_rating[0]
    rating = float(word_rating[1])
    print(word)
    user_rating = input()
    while user_rating < 1 or user_rating > 5:
        user_rating = input()
    if rating == -1:
        output_list.append([word,user_rating])
    else:
        output_list.append([word,(user_rating + rating)/2])

output_file = ""
for i in range(len(output_list)):
    output_file += output_list[i][0] + "," + output_list[i][1] + "\n"
    
file = open("word_list.txt","w") 

file.write(output_file)

file.close()
    
        
