from . import views
from django.urls import path
urlpatterns = [
    path("",views.print_tweets_list),
    path("api/v1/tweets",views.get_all_tweets_list),
    path("api/v1/users/<int:user_id>/tweets",views.get_tweets_list),
]
