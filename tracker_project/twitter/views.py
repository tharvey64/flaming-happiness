from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse
from twython import Twython
from pprint import pprint
from collections import Counter
from alchemyapi import AlchemyAPI
from tracker_project.settings import TWITTER_KEY
from tracker_project.settings import TWITTER_SECRET

class SearchView(View):
    template = 'twitter/index.html'
    pos = open('twitter/positive.txt')
    neg = open('twitter/negative.txt')   
    positivo = [line.strip().lower() for line in pos] 
    negativo = [line.strip().lower() for line in neg]
    alchemyapi = AlchemyAPI()


    def get(self, request):
       return render(request, self.template)

    def post(self, request):
        positive = 0
        negative = 0
        tweets = []
        actual_words = ''
        twitter = Twython(TWITTER_KEY, TWITTER_SECRET)
        result = twitter.search(q=request.POST['search'], count=5, result_type=request.POST['type'], lang='en') #everything
        start_point = result['statuses'] #one level into result... shouldnt have to use result again
        for tweet in start_point:
            if tweet['user']['followers_count'] > 5000:
                tweets.append(tweet['text']) # if user has more than 5k followers, we keep thier tweet
        broken_down = [line['entities'] for line in start_point] #hashtags 1
        almost_there = [block['hashtags'] for block in broken_down] #hashtags 2
        hashtags = [last[0]['text'].lower() for last in almost_there if len(last) > 0] #hashtags final
        for content in tweets:
            actual_words += content
        hash_dict = Counter(hashtags)
        top_hashes = hash_dict.most_common(5)
        for word in actual_words.split():
            if word.lower() in self.positivo:
                positive += 1
            elif word.lower() in self.negativo:
                negative += 1
        response = self.alchemyapi.sentiment("text", ('').join(actual_words))
        feeling = response.get("docSentiment")
        print (feeling)  
        if feeling == None:
            return JsonResponse({'result' : 'There was a problem searching for ' + request.POST['search'] + '. Please try a different filter.'})
        # return JsonResponse({'result': 'Your query returned ' + str(positive) +
        #                         ' positive keywords, and ' + str(negative) + ' negative keywords' +
        #                         ' People feel ' + feeling['type'] + ' about this topic.',
        #                     'hash': [{'name': hashe['text']} for hashe in start_point],
        #                     'hashes': [{'name': hashe[0]} for hashe in top_hashes]})
        return JsonResponse({'dates' : [{'date' : date['created_at']} for date in start_point], 
                            'feelings' : [{'feeling' : self.alchemyapi.sentiment("text", block)} for block in tweets], 
                            'favorites' : [{'favorite' : favorite['favorite_count']} for favorite in start_point]})


