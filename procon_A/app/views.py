from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import StudentAddForm
from .models import Student, Attendance, Event
from django.contrib.auth.decorators import login_required

def student_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            student = Student.objects.get(email=email, password=password)
            login(request, student)  # ログイン処理

            # 出席情報を保存
            Attendance.objects.create(student=student, attendance_time=timezone.now())

            return redirect('attendance_complete')  # 出席完了ページにリダイレクト
        except Student.DoesNotExist:
            messages.error(request, "ログイン情報が正しくありません。")

    return render(request, 'app/student_login.html')

def attendance_complete(request):
    return render(request, 'app/attendance_complete.html')  # 出席完了ページ

def student_attendance(request):
    # セッションから student_id を取得
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('student_login')  # 生徒が未ログインならログインページにリダイレクト

    # 生徒情報の取得
    student = Student.objects.get(id=student_id)

    if request.method == 'POST':
        # 出席情報を登録
        Attendance.objects.create(student=student, attendance_time=timezone.now())
        messages.success(request, '出席が完了しました。')
        return redirect('syusseki')  # 出席情報一覧ページにリダイレクト

    return render(request, 'app/student_attendance.html')

def syusseki(request):
    # 出席データを取得して表示
    attendances = Attendance.objects.select_related('student').all()
    return render(request, 'app/syusseki.html', {'attendances': attendances})

def students(request):
    return render(request, 'app/students.html')  # Servicesページ

def event(request):
    return render(request, 'app/event.html')  # Contactページ

def alert(request):
    return render(request, 'app/alert.html')

# 生徒追加フォームビュー
def add_student(request):
    if request.method == 'POST':
        form = StudentAddForm(request.POST)
        if form.is_valid():
            form.save()  # データベースに生徒情報を保存
            return redirect('students')
    else:
        form = StudentAddForm()

    return render(request, 'app/students_add.html', {'form': form})

def student_list(request):
    # データベースから全ての生徒を取得
    students = Student.objects.all()
    return render(request, 'app/students.html', {'students': students})

# イベント追加ビュー
def add_event(request):
    selected_month = 1
    if request.method == 'POST':
        month = int(request.POST['month'])
        day = int(request.POST['day'])
        event_time = request.POST['event_time']
        event_name = request.POST['event_name']
        event_note = request.POST['event_note']

        try:
            event_date = timezone.datetime(2024, month, day, int(event_time.split(':')[0]), int(event_time.split(':')[1]))
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

    months_range = range(1, 13)
    days_range = range(1, 29) if selected_month == 2 else (range(1, 31) if selected_month in [4, 6, 9, 11] else range(1, 32))
    times = [f'{h:02}:{m:02}' for h in range(24) for m in (0, 15, 30, 45)]

    context = {
        'months_range': months_range,
        'days_range': days_range,
        'times': times,
        'error_message': error_message,
        'selected_month': selected_month,
    }
    return render(request, 'app/event_add.html', context)

# イベント一覧ビュー
def event_list(request):
    events = Event.objects.all().order_by('event_date')
    context = {
        'events': events
    }
    return render(request, 'app/event.html', context)

# イベント削除ビュー
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event')  # イベント一覧ページへリダイレクト
