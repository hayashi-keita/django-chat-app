"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # http://localhost:8000/admin/ にアクセスすると、Djangoの**管理画面（Adminサイト）**にアクセスできる設定
    path('admin/', admin.site.urls),
    # 空のパス ''（= ルートURL http://localhost:8000/）にアクセスされたときに、作成したアプリ app 内の urls.py を呼び出すという意味
    path('', include('app.urls')),
]

# メディアファイルの表示設定
if settings.DEBUG:
    # 「開発中だけ、画像やアップロードされたファイル（MEDIA_URL）をMEDIA_ROOT フォルダから取り出して表示できるようにする」
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
