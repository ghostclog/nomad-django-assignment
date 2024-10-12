from . import views
from django.urls import path
urlpatterns = [
    path("",views.Tweets.as_view()),
    path("<int:pk>",views.TweetDetail.as_view()),
]
