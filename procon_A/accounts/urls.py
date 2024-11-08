from django.urls import path
from . import views
from .views import CustomLoginView, home
from django.contrib.auth.views import LogoutView  # 組み込みのログアウトビューをインポート

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),  # ログインページ
    path('logout/', LogoutView.as_view(), name='logout'),     # ログアウトURL
    path('home/', views.home_page, name='home'),  # ホームページ
    path('studenthome/', views.student_home, name='student_home'),  # 生徒用ホームページ
    path('logout/confirm/', views.student_logout_confirm, name='student_logout_confirm'),  # 確認ページのURL
]
