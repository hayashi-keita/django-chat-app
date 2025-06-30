from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .forms import PostForm, EventForm
from .models import Post, FriendshipRequest, ChatMessage, Event

# ホームページ
# ブラウザからアクセスがあると Django がビュー関数を呼び出しrequest という名前の引数にアクセス情報が自動的に入ってくる
@login_required  # ログインしていないとアクセスできない
# request は Djangoが自動でビュー関数に渡してくれる「HttpRequestオブジェクト」
def home_view(request):
    # 受信した未読メッセージをカウント
    unread_count = ChatMessage.objects.filter(receiver=request.user, is_read=False).count()
    return render(request, 'app/home.html', {'unread_count': unread_count})

# サインアップ画面の処理
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # ユーザ名の重複のチェック
        if User.objects.filter(username=username).exists():
            messages.error(request, 'このユーザー名は既に使用されています。')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'ユーザー登録が完了しました。ログインしてください。')
            return redirect('login')

    return render(request, 'app/signup.html')

# ログイン画面の処理
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # ユーザー認証
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'ログインしました。')
            return redirect('home')  # トップページにリダイレクト
        else:
            messages.error(request, 'ユーザー名またはパスワードが違います。')

    return render(request, 'app/login.html')

# ログアウト画面の処理
def logout_view(request):
    logout(request)
    return redirect('login')

# 投稿画面の処理
@login_required
def post_create_view(request):
    if request.method == 'POST':
        # 画像も扱うため request.FILES が必要
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # DB保存せずに一時停止
            post.author = request.user      # ログインユーザーを投稿者に設定、不正に他人を選ばれないように、ビューで自動設定
            post.save()                     # 保存
            return redirect('post_list')    # 投稿一覧ページへリダイレクト
    else:
        form = PostForm()

    return render(request, 'app/post_form.html', {'form': form})

# 投稿一覧画面の処理
@login_required
def post_list_view(request):
    posts = Post.objects.all().order_by('-created_at')  # 新しい順に並べる
    return render(request, 'app/post_list.html', {'posts': posts})

# 自分の投稿一覧画面の処理
@login_required
def my_posts_view(request):
    my_post = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'app/my_posts.html', {'posts': my_post})

# 投稿編集処理
@login_required
# pk は「編集したい投稿のID（主キー）」を受け取る
def post_edit(request, pk):
    # データベースから対象の投稿を取得、なければ 404 エラー（「投稿が見つかりません」）
    post = get_object_or_404(Post, pk=pk)
    # 本人以外はアクセス禁止
    if post.author != request.user:  # ログイン中なら：request.user は「ログインしているユーザーのUserインスタンス」
        return redirect('post_list')
    # 「保存ボタンを押した後」など、フォーム送信された場合
    if request.method == 'POST':
        # request.POST: フォームに入力されたテキストデータ
        # request.FILES: アップロードされた画像ファイル
        # instance=post: この投稿データを「上書き」するためのフォーム
        form = PostForm(request.POST, request.FILES, instance=post)
        # 入力に問題がなければ保存して、投稿一覧に戻る
        if form.is_valid():
            form.save()
            return redirect('my_posts')
    # 最初にページを開いたとき：フォームに投稿内容を表示（編集しやすく）
    else:
        form = PostForm(instance=post)
    # post_form.html テンプレートを表示し、フォームを画面に出す
    return render(request, 'app/post_form.html', {'form': form})

# 投稿削除処理
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 本人のみ削除できる
    if post.author != request.user:
        return redirect('post_list')

    post.delete()
    return redirect('my_posts')

# 友達申請送信の処理
@login_required
# user_id は URLパスから送られてきた申請先のユーザーID
def send_friend_request(request, user_id):
    # 申請相手のユーザーをIDから取得
    to_user = get_object_or_404(User, id=user_id)

    if request.user != to_user:
        # exists()で既に申請済み or 友達かを確認
        exists = FriendshipRequest.objects.filter(
            from_user=request.user,
            to_user=to_user,
        ).exists()

        if not exists:
            FriendshipRequest.objects.create(from_user=request.user, to_user=to_user)
            messages.success(request, f'{to_user.username}さんに友達申請を送りました！')
        else:
            messages.info(request, f'{to_user.username}さんには既に申請済です。')

    return redirect('user_list')  # ユーザー一覧など戻る先

# 友達申請一覧画面の処理
@login_required
def friend_requests(request):
    received_requests = request.user.received_requests.filter(is_approved=False)
    return render(request, 'app/friend_requests.html', {'requests': received_requests})

# 承認申請処理、受け手
@login_required
def approve_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendshipRequest, id=request_id, to_user=request.user)
    friend_request.is_approved = True
    friend_request.save()
    messages.success(request, f'{friend_request.from_user.username}さんの友達申請を承認しました。')
    return redirect('friend_requests')

# ユーザー一覧画面の処理
@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)  # 自分は除く
    return render(request, 'app/user_list.html', {'users': users})

# 友達一覧画面の処理
@login_required
def friend_list(request):
    user = request.user
    # 自分が送った申請のうち承認済
    sent = FriendshipRequest.objects.filter(from_user=user, is_approved=True)
    # 自分が受けた申請のうち承認済
    received = FriendshipRequest.objects.filter(to_user=user, is_approved=True)
    # 双方向に友達になっているユーザーを取得
    friends = list(set([fr.to_user for fr in sent] + [fr.from_user for fr in received]))

    # ✅ 各 friend に対して未読件数をカウント（辞書に格納）
    unread_counts = {}
    for friend in friends:
        count = ChatMessage.objects.filter(
            sender=friend,
            receiver=user,
            is_read=False,
        ).count()
        unread_counts[friend.id] = count

    return render(request, 'app/friend_list.html', {
        'friends': friends,
        'unread_counts': unread_counts,
        })

# チャット画面の処理
@login_required
def chat_view(request, user_id):
    # 友達データを取得
    friend = get_object_or_404(User, id=user_id)
    # 双方のメッセージを取得（時系列順に並べる）
    messages = ChatMessage.objects.filter(
        sender__in=[request.user, friend],
        receiver__in=[request.user, friend],
    ).order_by('timestamp')
    # 未読メッセージを既読にする（相手→自分 の未読）
    ChatMessage.objects.filter(
        sender=friend,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)
    # メッセージ送信処理
    if request.method == 'POST':
        msg = request.POST.get('message')
        if msg:
            ChatMessage.objects.create(
                sender=request.user,
                receiver=friend,
                message=msg
            )
            return redirect('chat', user_id=friend.id)

    return render(request, 'app/chat.html', {
        'friend': friend,
        'messages': messages,
        })

# 非同期通信
@login_required
@csrf_exempt
def send_message_ajax(request, user_id):
    if request.method == 'POST':
        friend = get_object_or_404(User, id=user_id)
        msg = request.POST.get('message')
        if msg:
            ChatMessage.objects.create(
                sender=request.user,
                receiver=friend,
                message=msg
            )

            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

# 新着メッセージ取得
@login_required
def get_messages_ajax(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    # 未読の相手からメッセージを取得
    new_messages = ChatMessage.objects.filter(
        sender=friend,
        receiver=request.user,
        is_read=False,
    ).order_by('timestamp')
    # メッセージをjsonで返す
    data = []
    for msg in new_messages:
        data.append({
            'sender': '自分' if msg.sender.id == request.user.id else msg.sender.username,
            'message': msg.message,
            'timestamp': msg.timestamp.strftime('%Y/%m%d %H:%M'),
        })

    return JsonResponse({'messages': data})

# チャット編集
@login_required
def edit_chat_message(request, user_id, message_id):
    message = get_object_or_404(ChatMessage, id=message_id, sender=request.user)

    if request.method == 'POST':
        new_message = request.POST.get('message')
        if new_message:
            message.message = new_message
            message.save()
            return redirect('chat', user_id=user_id)

    return render(request, 'app/edit_chat.html', {
        'message': message,
        'friend': get_object_or_404(User, id=user_id)
    })

# チャット削除
@login_required
def delete_chat_message(request, user_id, message_id):
    message = get_object_or_404(ChatMessage, id=message_id, sender=request.user)

    if request.method == 'POST':
        message.delete()
        return redirect('chat', user_id=user_id)

    return  render(request, 'app/delete_chat.html', {
        'message': message,
        'friend': get_object_or_404(User, id=user_id)
    })

# イベント機能
@login_required
def dashboard_view(request):
    today = timezone.now().date()
    month = today.month
    year = today.year

    events = Event.objects.filter(
        owner=request.user,
        date__year=year,
        date__month=month
    ).order_by('date')

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event.save()
            return redirect('dashboard')
    else:
        form = EventForm()

    return render(request, 'app/dashboard.html', {
        'form': form,
        'events': events,
        'today': today,
    })

# イベント一覧表示
@login_required
def event_list_view(request):
    events = Event.objects.filter(owner=request.user).order_by('date')
    return render(request, 'app/event_list.html', {'events': events})