from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Tweet,Like

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

    add_fieldsets = (
        (
            "유저 추가 정보",
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "user_nickname",
                    "email",
                    "birth",
                ),
            },
        ),
    )

    list_display = ("username", "user_nickname", "email", "is_premium")


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "트윗 정보",
            {
                "fields": (
                    "user",
                    "payload",
                ),
                "classes": ("wide",),
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")

    list_display = ("user", "payload", "created_at", "updated_at")
    search_fields = ("user__user_nickname", "payload")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "좋아요 정보",
            {
                "fields": (
                    "user",
                    "tweet",
                ),
                "classes": ("wide",),
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")

    list_display = ("user", "tweet", "created_at", "updated_at")
    search_fields = ("user__user_nickname", "tweet__payload")