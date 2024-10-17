from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render
from .forms import LoginForm

# カスタムログインビュー
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'  # ログインページのテンプレート
    authentication_form = LoginForm
    redirect_authenticated_user = True  # 認証済みユーザーをリダイレクト

    def get_success_url(self):
        return reverse_lazy('home')  # ログイン後のリダイレクト先

# ホームページビュー（テンプレートを使う）
def home(request):
    return render(request, 'accounts/home.html')  # home.html をレンダリング
