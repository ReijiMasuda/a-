from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import StudentAddForm
from .models import Student, Attendance, Event
from django.contrib.auth.decorators import login_required
import datetime


def add_student(request):
    if request.method == 'POST':
        form = StudentAddForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.registration_date = datetime.date.today()  # 現在の日付を設定
            student.save()  # データベースに保存
            return redirect('students')
    else:
        form = StudentAddForm()
    return render(request, 'app/students_add.html', {'form': form})


# def student_login(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         try:
#             student = Student.objects.get(email=email)
#             if student.password == password:  # パスワードを直接比較
#                 request.session['student_id'] = student.id  # student_idをセッションに保存

#                 # 出席情報を保存（必要であれば）
#                 Attendance.objects.create(student=student, attendance_time=timezone.now())

#                 return redirect('student_attendance')  # 出席登録ページにリダイレクト
#             else:
#                 messages.error(request, "ログイン情報が正しくありません。")
#         except Student.DoesNotExist:
#             messages.error(request, "ログイン情報が正しくありません。")

#     return render(request, 'app/student_login.html')


def student_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            student = Student.objects.get(email=email)
            if student.password == password:  # パスワードを直接比較
                request.session['student_id'] = student.id  # student_idをセッションに保存

                # 出席情報を取得または作成
                attendance, created = Attendance.objects.get_or_create(student=student)

                # 新規作成でなくても出席情報を「出席」に更新
                attendance.status = '〇'  # 出席に設定
                attendance.save()  # 更新を保存

                return redirect('student_attendance')  # 出席登録ページにリダイレクト
            else:
                messages.error(request, "ログイン情報が正しくありません。")
        except Student.DoesNotExist:
            messages.error(request, "ログイン情報が正しくありません。")

    return render(request, 'app/student_login.html')


def student_attendance(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('student_login')  # 生徒が未ログインならログインページにリダイレクト

    # 生徒情報の取得
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        # 出席情報を登録
        Attendance.objects.create(student=student, attendance_time=timezone.now())
        messages.success(request, '出席が完了しました。')
        return redirect('syusseki')  # 出席情報一覧ページにリダイレクト

    return render(request, 'app/attendance_complete.html')


def syusseki(request):
    # 登録されているすべての生徒を取得
    students = Student.objects.all()

    # ログイン中の生徒が出席した場合の情報を取得
    logged_in_student_id = request.session.get('student_id')
    attendances = Attendance.objects.filter(student__in=students)  # `student_id` ではなく `student` で絞り込み

    # 出席状況を格納
    student_statuses = []
    for student in students:
        attendance = attendances.filter(student=student).first()  # 出席情報を1件取得
        status = attendance.status if attendance else '×'  # 出席情報がなければデフォルトで欠席

        is_logged_in = student.id == logged_in_student_id
        student_statuses.append({
            'student': student,
            'status': status,
            'is_logged_in': is_logged_in,
        })

    return render(request, 'app/syusseki.html', {'student_statuses': student_statuses})


def students(request):
    return render(request, 'app/students.html')  # Servicesページ

def event(request):
    return render(request, 'app/event.html')  # Contactページ

def alert(request):
    return render(request, 'app/alert.html')

# # 生徒追加フォームビュー
# def add_student(request):
#     if request.method == 'POST':
#         form = StudentAddForm(request.POST)
#         if form.is_valid():
#             form.save()  # データベースに生徒情報を保存
#             return redirect('students')
#     else:
#         form = StudentAddForm()

#     return render(request, 'app/students_add.html', {'form': form})


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



def edit_student(request, student_id):
    # 編集する生徒を取得
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        # フォーム送信内容を保存
        form = StudentAddForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')  # 編集後に生徒一覧にリダイレクト
    else:
        # 現在の生徒情報をフォームに表示
        form = StudentAddForm(instance=student)

    return render(request, 'app/edit_student.html', {'form': form, 'student': student})


def edit_attendance(request, student_id):
    # 生徒情報を取得
    student = get_object_or_404(Student, id=student_id)

    # 出席情報を取得、無ければ新規作成
    attendance, created = Attendance.objects.get_or_create(student=student)

    if request.method == 'POST':
        # POSTリクエストがあった場合、出席状況を更新
        status = request.POST.get('status')
        attendance.status = status
        attendance.save()

        messages.success(request, f'{attendance.student.name}の出席状況が更新されました。')
        return redirect('syusseki')  # 出席状況一覧にリダイレクト

    return render(request, 'app/edit_attendance.html', {'attendance': attendance, 'student': attendance.student})
