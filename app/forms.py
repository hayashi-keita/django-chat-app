from django import forms
from .models import Post

# ModelForm は「モデルと連動するフォーム」を意味
class PostForm(forms.ModelForm):
    # この中で「どのモデルに基づいたフォームか」などを指定
    class Meta:
        # 投稿フォームはこの Post モデルの内容を元に作成
        # モデルで content（本文）と image（画像）があれば、その内容に応じて自動的に HTMLフォームが作られる
        model = Post  # このフォームは Post モデル（＝投稿内容）に対応している、という意味
        # モデルの中から、このフォームクラスに表示させるフィールド（項目）を選ぶ
        fields = ['content', 'image']  # 投稿文、画像
        # 各フィールドの見た目（HTMLの入力欄）をカスタマイズ
        # content の入力欄は 4行のテキストエリア、入力欄の中に「内容を入力してください」と表示される（プレースホルダー）
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': '内容を確認してください'}),
        }