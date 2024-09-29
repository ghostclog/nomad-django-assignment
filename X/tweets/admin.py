from django.contrib import admin
from .models import Tweet,Like

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