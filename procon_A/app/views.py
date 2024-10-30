from django.shortcuts import render, redirect
from .forms import StudentAddForm
from .models import Student
from .models import Event
import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .models import Student, Attendance  # Attendanceモデルを追加
from django.shortcuts import render, redirect
from app.models import Student  # 必要に応じてアプリ名を置き換え

def student_login(request):
    # Studentモデルの利用例
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            student = Student.objects.get(email=email, password=password)
            # ログイン処理
            return redirect('attendance_page')  # 適切なURLにリダイレクト
        except Student.DoesNotExist:
            # エラーハンドリング
            pass

    return render(request, 'student_login.html')


def student_attendance(request):
    if request.method == 'POST':
        student = request.user
        Attendance.objects.create(student=student, attendance_time=timezone.now())  # 出席情報を保存
        messages.success(request, '出席が完了しました。')
    
    return render(request, 'app/student_attendance.html')

def syusseki(request):
    attendances = Attendance.objects.select_related('student').all()
    return render(request, 'app/syusseki.html', {'attendances': attendances})

def students(request):
    return render(request, 'app/students.html')  # Servicesページ

def event(request):
    return render(request, 'app/event.html')  # Contactページ

def alert(request):
    return render(request, 'app/alert.html')  # FAQページ


def add_student(request):
    if request.method == 'POST':
        form = StudentAddForm(request.POST)
        if form.is_valid():
            form.save()  # データベースに生徒情報を保存
            return redirect('students')  # 生徒一覧ページなどにリダイレクト
        else:
            form.errors.clear()
    else:
        form = StudentAddForm()

    return render(request, 'app/students_add.html', {'form': form})

def student_list(request):
    # データベースから全ての生徒を取得
    students = Student.objects.all()
    return render(request, 'app/students.html', {'students': students})

def add_event(request):
    # デフォルトの月を1に設定
    selected_month = 1
    if request.method == 'POST':
        month = int(request.POST['month'])
        day = int(request.POST['day'])
        event_time = request.POST['event_time']
        event_name = request.POST['event_name']
        event_note = request.POST['event_note']

        # イベントの日付と開始時間を設定
        try:
            event_date = timezone.datetime(2024, month, day, int(event_time.split(':')[0]), int(event_time.split(':')[1]))
            # イベントをデータベースに追加
            Event.objects.create(
                event_date=event_date,
                event_name=event_name,
                event_note=event_note
            )
            return redirect('event')  # イベント一覧ページへリダイレクト

        except ValueError:
            error_message = "無効な日付です。正しい日付を選択してください。"

    else:
        selected_month = int(request.GET.get('month', 1))
        error_message = None

    # 月のプルダウン選択肢（1月～12月）
    months_range = range(1, 13)

    # 選択された月に基づいて日数を設定
    if selected_month == 2:
        days_range = range(1, 29)  # 2月は28日まで
    elif selected_month in [4, 6, 9, 11]:
        days_range = range(1, 31)  # 4, 6, 9, 11月は30日まで
    else:
        days_range = range(1, 32)  # それ以外の月は31日まで

    # 開始時間のプルダウン選択肢（15分おき）
    times = [f'{h:02}:{m:02}' for h in range(24) for m in (0, 15, 30, 45)]

    context = {
        'months_range': months_range,
        'days_range': days_range,
        'times': times,
        'error_message': error_message,
        'selected_month': selected_month,
    }
    return render(request, 'app/event_add.html', context)

def event_list(request):
    events = Event.objects.all().order_by('event_date')  # イベントを取得し、日付でソート
    context = {
        'events': events
    }
    return render(request, 'app/event.html', context)

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event')  # イベント一覧ページへリダイレクト
