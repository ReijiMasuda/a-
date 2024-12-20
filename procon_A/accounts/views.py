from .forms import LoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render
import qrcode
from io import BytesIO
import base64
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'  # ログインページのテンプレート
    authentication_form = LoginForm
    redirect_authenticated_user = True  # 認証済みユーザーをリダイレクト

    def get_success_url(self):
        return reverse_lazy('home')  # ログイン後のリダイレクト先

    # ログイン失敗時にエラーメッセージを追加
    def form_invalid(self, form):
        form.errors.clear()
        messages.error(self.request, 'ログインに失敗しました。ユーザー名またはパスワードが間違っています。')
        return super().form_invalid(form)
    
    # ホームページビュー（テンプレートを使う）
def home(request):
    return render(request, 'accounts/home.html')  # home.html をレンダリング

# 生徒用ホームページビュー
def student_home(request):
    return render(request, 'accounts/student_home.html')  # student_home.html をレンダリング

def student_logout_confirm(request):
    # 確認ページを表示するためのビュー
    return render(request, 'accounts/student_logout.html')

def generate_qr_code(data):
    # QRコードの生成
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    
    # 画像をバイナリストリームに保存
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    # バイナリデータをbase64エンコード
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_str

#
# def home_page(request):
#     qr_data = "https://example.com/attendance"  # QRコードに含めるデータ
#     qr_code = generate_qr_code(qr_data)
#
#     current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#
#     context = {
#         'qr_code': qr_code,
#         'current_time': current_time
#     }
#     return render(request, 'accounts/home.html', context)

def home_page(request):
    qr_data = request.build_absolute_uri(reverse_lazy('student_login'))  # 生徒ログイン用URLをQRコードに設定
    qr_code = generate_qr_code(qr_data)
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    context = {
        'qr_code': qr_code,
        'current_time': current_time
    }
    return render(request, 'accounts/home.html', context)
