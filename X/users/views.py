from .models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,UserRegistSerializer
from tweets.serializers import TweetSerializer
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_204_NO_CONTENT,HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_201_CREATED
from rest_framework.exceptions import NotFound,ParseError,PermissionDenied

# 모든 유저 / 유저 생성
class AllUsers(APIView):
    def get(self,request): # 모든 유저 정보 반환
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)

    def post(self,request): # 유저 생성
        serializer = UserRegistSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            serializer = UserRegistSerializer(user)
            return Response(serializer.data,status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

# 유저 상세 정보
class DetailUser(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except:
            raise NotFound
    # 유저 상세 정보 보기
    def get(self,request,pk):
        user = self.get_object(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data,status=HTTP_200_OK)
    # 유저 정보 수정(추가로 만든 코드)
    def put(self,request,pk):
        user = self.get_object(pk=pk)
        if request.user.username != user.username:
            raise PermissionDenied
        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            edit_user = serializer.save()
            return Response(serializer.data,status=HTTP_200_OK)
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
    # 특정 유저 삭제(회원탈퇴 / 추가로 만든 코드)
    def delete(self, request):
        if request.user:
            request.user.delete()
            return Response({"response":"회원 탈퇴가 정상적으로 이루워졌습니다."},status= HTTP_204_NO_CONTENT)
        raise PermissionDenied
    
# 특정 유저 작성 트윗
class UserTweet(APIView):
    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self,request,pk):
        user = self.get_object(pk)
        serializer = TweetSerializer(user.tweets.all(),many=True)
        return Response(serializer.data,status=HTTP_200_OK)

# 비번 변경
class Password(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = request.user
        old_password = request.data.get("old_password") # 기존 비번
        new_password = request.data.get("new_password") # 새로 설정할 비번
        chk_password = request.data.get("chk_password") # 검증용 비번
        if not user.check_password(old_password): # DB의 비번과 사용자 입력 기존 비번 체크
            return Response({"response":"비밀번호가 일치하지 않습니다."},status=HTTP_400_BAD_REQUEST)
        if (new_password != chk_password): # 신규 비번과 검증용 비번 체크
            return Response({"response":"신규 비밀번호와 검증 비밀번호가 일치하지 않습니다."},status=HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        serializer = UserRegistSerializer(user)
        return Response(serializer.data,status=HTTP_201_CREATED)

# 로그인
class Login(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"response": f"로그인 성공! 어서오세요. {user.user_nickname}님!"},status=HTTP_200_OK)
        else:
            return Response({"response": "로그인 실패. 아이디 혹은 비밀번호를 재확인해주세요."},status=HTTP_400_BAD_REQUEST)


# 로그아웃
class Logout(APIView):
    # 권한 체크. 상식적으로 로그인 안된 유저가 로그아웃을 할 수 있을리가 없잖아요?
    permission_classes = [IsAuthenticated] 
    def post(self, request):
        logout(request)
        return Response({"response": "로그아웃 되었습니다!"})
    