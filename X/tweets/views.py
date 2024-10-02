from django.shortcuts import render
from .models import Tweet
# Create your views here.

def print_tweets_list(request):
    return render(
        request,
        "test.html",
        {
            "datas":Tweet.objects.all()
        }
    )
