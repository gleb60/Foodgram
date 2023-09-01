from django.contrib import admin

from .models import User, Follow


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
    )
    ordering = (
        'email',
    )
    search_fields = (
        'username',
        'email',
        'first_name',
    )
    list_filter = (
        'username',
        'first_name',
        'last_name',
        'email',
    )


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author',
    )
    ordering = (
        'user',
    )
    search_fields = (
        'user__username',
    )


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
