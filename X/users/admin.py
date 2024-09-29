from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "프로필 기본 정보",
            {
                "fields": (
                    "username",
                    "password", 
                    "user_nickname", 
                    "email", 
                    "my_comment",
                    "location",
                    "website",
                    "birth",
                    "date_joined",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "유저 이미지 정보",
            {
                "fields": (
                    "profile_image", 
                    "profile_banner",
                    ),
                "classes": ("wide",),
            },
        ),
        (
            "계정 특수 정보",
            {
                "fields": (
                    "is_profesional",
                    "is_premium",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "계정 권한 정보",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    list_display = ("username", "user_nickname", "email", "is_premium")