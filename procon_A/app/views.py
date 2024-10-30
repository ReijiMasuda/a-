from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import StudentAddForm
from .models import Student
from .models import Event
import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

def syusseki(request):
    return render(request, 'app/syusseki.html')  # Aboutページ

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
