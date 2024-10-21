from .forms import LoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render
import qrcode
from io import BytesIO
import base64
from datetime import datetime
import secrets
from django.urls import reverse
from django.contrib.auth.decorators import login_required
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

def generate_qr_code(data):
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
 
@login_required
def home_page(request):
    # ランダムなトークンを生成
    random_token = secrets.token_urlsafe(16)  # 16バイトのランダムなトークン
 
    # トークンをセッションに保存（後で確認するため）
    request.session['qr_token'] = random_token
 
    # QRコードに学生用のログインページのURLとランダムトークンを含める
    login_url = reverse('student_login')  # 'student_login' という名前のURL
    # ドメイン名を動的に取得
    domain = request.build_absolute_uri('/')[:-1]  # ドメイン名を取得
    qr_data = f"{domain}{login_url}?next=/attendance_confirm/?token={random_token}"
 
    # QRコードの生成
    qr_code = generate_qr_code(qr_data)
 
    # 現在の時刻を取得
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 
    context = {
        'qr_code': qr_code,
        'current_time': current_time
    }
 
    return render(request, 'accounts/home.html', context)