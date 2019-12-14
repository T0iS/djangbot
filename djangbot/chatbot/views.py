from django.shortcuts import render
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from .models import Files
import json
import requests
from subprocess import run, PIPE
import sys


# Create your views here.


def home(request):

    return render(request, "chatbot/home.html")


def about(request):

    return HttpResponse("HEY")


def rendering(request):
    return render(request, "chatbot/botpage.html", {})


def bot(request):
    msg = ""
    if request.method == "POST":
        if "data" in request.POST:
            msg = request.POST["data"]
            from newspaper import Article
            import random
            import string
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            import nltk
            import numpy as np
            import warnings

            warnings.filterwarnings("ignore")

            nltk.download("punkt", quiet=True)
            nltk.download("wordnet", quiet=True)


            articles = Files.objects.values('url')
            text = ""
            for art in articles:
                article = Article (art['url'])
                article.download()
                article.parse()
                article.nlp()
                corpus = article.text
                text += corpus
                text +="\n\n"

            

            
            sent_tokens = nltk.sent_tokenize(text)

            remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

            def LemNorm(text):
                return nltk.word_tokenize(text.lower().translate(remove_punct_dict))

            greeting_inputs = [
                "hi",
                "hello",
                "hola",
                "greetings",
                "wassup",
                "hey",
                "ahoj",
                "cus",
            ]
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
                    bot_response = (
                        bot_response + "I apologize, I do not understand that.\n Try using /addarticle command and pass me a link so I can learn :-)"
                    )
                else:
                    bot_response = bot_response + sent_tokens[idx]

                # print(bot_response)

                sent_tokens.remove(user_response)

                return bot_response

            flag = True
            # print("T_BOT: Ask me anything!")

            # while flag == True:
            user_response = msg
            user_response = user_response.lower()

            if user_response != "bye":
                if user_response == "thanks" or user_response == "thank you":
                    flag = False
                    print("T_BOT: No problem")
                    msg = "T_BOT: No problem"
                else:
                    if greet(user_response) != None:
                        print("T_BOT: " + greet(user_response))
                        msg = "T_BOT: " + greet(user_response)
                    elif "/addarticle" in user_response:
                        user_response = user_response.strip("/addarticle ")
                        newart = Files(url=user_response)
                        newart.save()
                    else:
                        print("T_BOT: " + resp(user_response))
                        msg = "T_BOT: " + resp(user_response)

            else:
                flag = False
                print("T_BOT: Cy@!")
                msg = "T_BOT: Cy@!"

    return HttpResponse(msg)
