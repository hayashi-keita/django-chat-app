from django.contrib import admin
from .models import Post, FriendshipRequest

admin.site.register(Post)
admin.site.register(FriendshipRequest)