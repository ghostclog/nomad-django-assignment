from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# 왠지 트위터(X) 클론코딩하는거 같아서, user모델을 트위터(X)랑 어느정도 똑같이 모델을 구성했습니다.
class User(AbstractUser):
    # 비활성화 컬럼
    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    
    # 활성화 컬럼    
    user_nickname = models.CharField(max_length=50)
    my_comment = models.CharField(max_length=160, default="")
    location = models.CharField(max_length=30,default="")
    website = models.CharField(max_length=100,default="")
    is_premium = models.BooleanField(default=False)
    birth = models.DateField()
    is_profesional = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to="/profile_image")
    profile_banner = models.ImageField(upload_to="/profile_banner")


    def __str__(self):
        return self.user_nickname

class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Tweet(AbstractModel):
    payload = models.CharField(max_length=180)
    user = models.ForeignKey(User,related_name="tweet")

    def __str__(self):
        return self.payload

class Like(AbstractModel):
    tweet = models.ForeignKey(Tweet)
    user = models.ForeignKey(User,related_name="like")

    def __str__(self):
        user_name = self.user.user_nickname
        tweet_contents = self.tweet.payload

        return f"{user_name} like The '{tweet_contents}'"