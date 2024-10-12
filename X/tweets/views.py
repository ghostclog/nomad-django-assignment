from .models import Tweet
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TweetSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound,PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT,HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_201_CREATED

# 전체 트윗보기, 트윗 생성하기
class Tweets(APIView):
    # 권한 체크. 권한 없으면 읽기 전용

    def get(self,request): #모든 트윗 보여주기
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(tweets,many=True)
        return Response(serializer.data,status=HTTP_200_OK)

    def post(self, request):  # 트윗 만들기
        serializer = TweetSerializer(data=request.data)
        if serializer.is_valid():
            tweet = serializer.save(user=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
            

# 특정 트윗 보기, 특정 트윗 수정하기, 특정 트윗 삭제하기
class TweetDetail(APIView):
    # 권한 체크. 권한 없으면 읽기 전용
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self,pk): # 단일 트윗 객체 받아오기
        try:
            return Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            raise NotFound
        
    def get(self,request,pk): # 특정 트윗 정보 받아오기
        tweet = self.get_object(pk)
        serializer = TweetSerializer(tweet)
        return Response(serializer.data,status=HTTP_200_OK)

    def put(self,request,pk): # 특정 트윗 수정하기
        tweet = self.get_object(pk)
        if(tweet.user == request.user):
            serializer = TweetSerializer(
                tweet,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                edit_tweet = serializer.save()
                return Response(serializer.data,status=HTTP_200_OK)
            else:
                return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied

    def delete(self,request,pk): # 특정 트윗 삭제하기
        tweet = self.get_object(pk)
        tweet.delete()
        return Response(status=HTTP_204_NO_CONTENT)