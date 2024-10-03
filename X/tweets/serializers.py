from rest_framework import serializers

class TweetSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    payload = serializers.CharField(max_length=180)
    user_nickname = serializers.CharField(source='user.user_nickname', read_only=True)

    