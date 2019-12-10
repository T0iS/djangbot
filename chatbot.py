from newspaper import Article
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import numpy as np
import warnings
import sys


warnings.filterwarnings("ignore")

nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)


article = Article(
    "https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521"
)
article.download()
article.parse()
article.nlp()
corpus = article.text


text = corpus
sent_tokens = nltk.sent_tokenize(text)


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNorm(text):
    return nltk.word_tokenize(text.lower().translate(remove_punct_dict))


greeting_inputs = ["hi", "hello", "hola", "greetings", "wassup", "hey"]
greetings_resp = ["howdy", "hi", "hey", "what's good", "hey there", "hello"]


def greet(sentence):
    for word in sentence.split():
        if word.lower() in greeting_inputs:
            return random.choice(greetings_resp)


def resp(user_response):

    # user_response = "what is chronic kidney disease"
    user_response = user_response.lower()
    bot_response = ""

    sent_tokens.append(user_response)

    TfidfVec = TfidfVectorizer(tokenizer=LemNorm, stop_words="english")

    tfidf = TfidfVec.fit_transform(sent_tokens)

    vals = cosine_similarity(tfidf[-1], tfidf)

    idx = vals.argsort()[0][-2]

    flat = vals.flatten()
    flat.sort()

    score = flat[-2]

    if score == 0:
        bot_response = bot_response + "I apologize, I do not understand that."
    else:
        bot_response = bot_response + sent_tokens[idx]

    # print(bot_response)

    sent_tokens.remove(user_response)

    return bot_response


flag = True
print("T_BOT: Ask me anything!")


while flag == True:
    user_response = sys.argv[1]
    user_response = user_response.lower()

    if user_response != "bye":
        if user_response == "thanks" or user_response == "thank you":
            flag = False
            print("T_BOT: No problem")
        else:
            if greet(user_response) != None:
                print("T_BOT: " + greet(user_response))
            else:
                print("T_BOT: " + resp(user_response))

    else:
        flag = False
        print("T_BOT: Cy@!")
