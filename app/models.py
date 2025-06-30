from django.db import models
from django.contrib.auth.models import User

# 投稿モデル
class Post(models.Model):
    # オブジェクトを削除された時、残すか消すかを決める
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 例: ブログの記事を消したらそこに寄せられたコメントも必要ないから消す
    content = models.TextField()
    # 画像を post_images/ ディレクトリに保存する、フィールドが空もnullも許容する
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    # auto_now_add=Trueとすると、最初の1回だけそのタイミングの日時を登録し、その後は更新されない
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} の投稿 ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

# 友達申請・承認モデル
class FriendshipRequest(models.Model):
    # 申請を送った人 ユーザーが削除されたときに、on_delete=models.CASCADEそのユーザーが関わっていた申請も一緒に削除する、という設定
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    # 申請を受けた人
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')  # 重複申請防止

    def __str__(self):
        status = '承認済' if self.is_approved else '未承認'
        return f"{self.from_user.username} → {self.to_user.username} ({status})"

# チャットモデル
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.sender.username} → {self.receiver.username}: {self.message[:20]}'

# イベント機能
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} ({self.date})'