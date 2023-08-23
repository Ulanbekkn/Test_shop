from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import VerifyCode, Favorite


@admin.register(VerifyCode)
class VerifyCodeAdmin(ModelAdmin):
    pass


@admin.register(Favorite)
class FavoriteAdmin(ModelAdmin):
    pass
