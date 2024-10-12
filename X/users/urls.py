from . import views
from django.urls import path
urlpatterns = [
    path("",views.AllUsers.as_view()),
    path("<int:pk>",views.DetailUser.as_view()),
    path("<int:pk>/tweets",views.UserTweet.as_view()),
    path("password",views.Password.as_view()),
    path("login",views.Login.as_view()),
    path("logout",views.Logout.as_view()),
]
