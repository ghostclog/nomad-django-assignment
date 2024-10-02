from . import views
from django.urls import path
urlpatterns = [
    path("",views.print_tweets_list)
]
