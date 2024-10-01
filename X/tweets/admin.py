from django.contrib import admin
from .models import Tweet,Like
from django.utils.translation import gettext_lazy

class KeywordFilter(admin.SimpleListFilter):
    title = "Filter by keywords!"

    parameter_name = "filter_keyword"

    def lookups(self, request, model_admin):
        return [
            ("contain", 'Contains "Elon Musk"'),
            ("not_contain", 'Does not contain "Elon Musk"'),
        ]

    def queryset(self, request, tweet):
        keyword = "Elon Musk"
        if self.value() == 'contain':
            return tweet.filter(payload__icontains=keyword)
        elif self.value() == 'not_contain':
            return tweet.exclude(payload__icontains=keyword)
        return tweet

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
    list_filter = ("created_at",KeywordFilter)
    list_display = ("__str__","user", "payload", "like_tweets", "created_at", "updated_at")
    search_fields = ("user__username","user__user_nickname", "payload")


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
    list_filter = ("created_at",)
    list_display = ("__str__","user", "tweet", "created_at", "updated_at")
    search_fields = ("user__username","user__user_nickname", "tweet__payload")