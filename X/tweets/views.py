from django.shortcuts import render
from .models import Tweet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import User
from .serializers import TweetSerializer
# Create your views here.

def print_tweets_list(request):
    return render(
        request,
        "test.html",
        {
            "datas":Tweet.objects.all()
        }
    )

@api_view(["GET"])
def get_all_tweets_list(request):
    tweets = Tweet.objects.all()
    serializer = TweetSerializer(tweets,many=True)
    return Response({"result": "exist", "data": serializer.data})

@api_view(["GET"])
def get_tweets_list(request,user_id):
    try: 
        user = User.objects.filter(id=user_id).get(pk = user_id)
        try:
            tweet = Tweet.objects.filter(user = user)
            serializer = TweetSerializer(tweet,many=True)
            return Response({"result": "exist", "data": serializer.data})
        except:
            return Response({"result": "tweets not found","data": ""})
    except User.DoesNotExist:
        raise Response({"result": "user not found","data": ""})