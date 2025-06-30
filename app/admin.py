from django.contrib import admin
from .models import Post, FriendshipRequest, ChatMessage

admin.site.register(Post)
admin.site.register(FriendshipRequest)
admin.site.register(ChatMessage)