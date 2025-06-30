from .models import ChatMessage

def unread_count(request):
    if request.user.is_authenticated:
        count = ChatMessage.objects.filter(receiver=request.user, is_read=False).count()
    else:
        count = 0
    return {'unread_count': count}