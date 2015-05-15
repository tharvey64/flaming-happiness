from django.db import models
from django.conf import settings
from sentiment.models import Sentiment
# Create your models here.

class Tweet(models.Model):
    text = models.CharField(max_length=180)
    tweet_id = models.BigIntegerField()
    favorites = models.IntegerField()
    tweet_date = models.DateTimeField()
    keyword = models.CharField(max_length=200)
    sentiment = models.ForeignKey(Sentiment)

class Profile(models.Model):
    token = models.CharField(max_length=180)
    secret = models.CharField(max_length=180)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)