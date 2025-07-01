# app/urls.py
from django.urls import path
from . import views

# パスの設定
urlpatterns = [
    path('', views.home_view, name='home'),  # ホームページ（アクセス時の画面）
    path('signup/', views.signup_view, name='signup'),  # サインアップページ
    path('login/', views.login_view, name='login'),  # ログインページ
    path('logout/', views.logout_view, name='logout'),  # ログアウト→ログイン画面に戻る
    path('post/new/', views.post_create_view, name='post_create'),  # 投稿作成ページ、テンプレート内で {% url 'post_create' %} と呼び出せる
    path('posts/', views.post_list_view, name='post_list'),  # 投稿一覧ページ
    path('my_posts/', views.my_posts_view, name='my_posts'),  # 自分の投稿一覧ページ
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),  # 投稿編集
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),  # 投稿削除
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),  # 友達申請
    path('friend_requests/', views.friend_requests, name='friend_requests'),  # 友達申請一覧ページ
    path('approve_friend_request/<int:request_id>/', views.approve_friend_request, name='approve_friend_request'),  # 承認申請
    path('users/', views.user_list, name='user_list'),  # ユーザー一覧ページ
    path('friends/', views.friend_list, name='friend_list'),  # 友達一覧ページ
    path('chat/<int:user_id>/', views.chat_view, name='chat'),  # チャットページ
    path('chat/<int:user_id>/send/', views.send_message_ajax, name='send_message_ajax'),  # 非同期通信
    path('chat/<int:user_id>/messages/', views.get_messages_ajax, name='get_messages_ajax'),  # 未読既読
    path('chat/<int:user_id>/<int:message_id>/edit', views.edit_chat_message, name='edit_chat'),  # チャット編集
    path('chat/<int:user_id>/<int:message_id>/delete', views.delete_chat_message, name='delete_chat'),  # チャット削除
    path('dashboard/', views.dashboard_view, name='dashboard'),  #  ダッシュボードページ
    path('events/', views.event_list_view, name='event_list'),  # イベント一覧ページ
    path('events/<int:pk>/edit/', views.edit_event_view, name='edit_event'),  #イベント編集ページ
    path('events/<int:pk>/delete/', views.delete_event_view, name='delete_event')  # イベント削除
]