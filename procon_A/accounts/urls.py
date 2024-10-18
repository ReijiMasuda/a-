from django.urls import path
from . import views
from .views import CustomLoginView, home
from django.contrib.auth.views import LogoutView  # 組み込みのログアウトビューをインポート

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),  # ログインページ
    path('logout/', LogoutView.as_view(), name='logout'),     # ログアウトURL
    path('home/', views.home_page, name='home'),  # ホームページ
]
