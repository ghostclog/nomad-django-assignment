from rest_framework import serializers
from users.serializers import SimpleUserSrializer
from .models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    like_tweets = serializers.SerializerMethodField()
    user = SimpleUserSrializer(read_only=True)
    
    class Meta:
        model = Tweet
        fields = "__all__"

    def get_like_tweets(self,tweets):
        return tweets.like_tweets()
    
