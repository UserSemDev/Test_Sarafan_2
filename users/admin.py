from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'is_active', 'date_joined')
    list_filter = ('is_active',)
    search_fields = ('email',)
