from rest_framework import serializers
from .models import User

class SimpleUserSrializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'user_nickname',
            'is_premium',
            'profile_image',
        )

# 유저 등록시에 사용되는 시리얼라이저 / 객체 생성 단계에서 비밀번호를 해싱하게 설정
class UserRegistSerializer(serializers.ModelSerializer):
    location = serializers.CharField(required=False, allow_blank=True)
    birth = serializers.DateField(required=False, allow_null=True)   

    class Meta:
        model = User
        fields =(
            "username",
            "password",
            "user_nickname",
            "location",
            "birth",
        )
        
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            user_nickname=validated_data['user_nickname'],
            location=validated_data.get('location', '비공개'),
            birth=validated_data.get('birth', None)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# 유저 상세 정보 제공 및 유저 데이터 수정 시에 사용
class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)
    profile_banner = serializers.ImageField(required=False)
    birth = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = "__all__"
