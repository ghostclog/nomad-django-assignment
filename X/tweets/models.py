from django.db import models


# Create your models here.

class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Tweet(AbstractModel):
    payload = models.CharField(max_length=180)
    user = models.ForeignKey(
        "users.User",
        related_name="tweet",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.payload
    
    def like_tweets(self):
        return self.like.count()

class Like(AbstractModel):
    tweet = models.ForeignKey(
        "tweets.Tweet",
        related_name="like",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "users.User",
        related_name="like",
        on_delete=models.CASCADE
    )

    def __str__(self):
        user_name = self.user.user_nickname
        tweet_contents = self.tweet.payload

        return f"{user_name} like The '{tweet_contents}'"