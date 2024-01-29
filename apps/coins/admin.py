# coins/admin.py
from django.contrib import admin
from .models import UserCoins

@admin.register(UserCoins)
class UserCoinsAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'last_updated')
    search_fields = ('user__username',)
