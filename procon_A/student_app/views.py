from django.shortcuts import render
from django.shortcuts import render, redirect
from datetime import datetime
from .models import AttendanceRecord
from app.models import Event
from student_app.models import DeletedEvent
from django.urls import reverse

def student_event_list(request):
    # 削除されたイベントを取得(11/29 イベント取り消しのページはデータベースを作ってからやる)
    deleted_event = DeletedEvent.objects.last()
    if deleted_event:
        # 削除通知ページにリダイレクト
        return redirect('app/students_eventalert.html')
    
        # 通常のイベントリストを表示
    events = Event.objects.all()
    return render(request, 'app/students_event.html', {'events': events})

def students_eventalert(request):
    deleted_event = DeletedEvent.objects.last()
    return render(request, 'app/students_eventalert.html', {
        'deleted_event': deleted_event})

def students_calendar(request):
    return render(request, 'app/students_calendar.html')

def students_report(request):
    # クエリパラメータ 'date' を取得
    date_str = request.GET.get('date')
    
    # 文字列を datetime オブジェクトに変換
    date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else None

    context = {
        'date': date,  # datetime オブジェクトをテンプレートに渡す
    }
    return render(request, 'app/students_report.html', context)


def students_reportcomplete(request):
    return render(request, 'app/students_reportcomplete.html')

def students_admin_return(request):
    return render(request, 'app/students_admin_return.html')

# カレンダー機能
def attendance_view(request):
    # 現在の月と年
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    
    # 月間データ集計
    monthly_records = AttendanceRecord.objects.filter(
        date__year=current_year,
        date__month=current_month
    )
    monthly_stats = calculate_attendance_stats(monthly_records)
    
    # 年間データ集計
    yearly_records = AttendanceRecord.objects.filter(
        date__year=current_year
    )
    yearly_stats = calculate_attendance_stats(yearly_records)

    # カレンダーイベントデータを作成
    calendar_data = [
        {
            'title': '出席' if record.status == 'attended' else '欠席' if record.status == 'absent' else '遅刻' if record.status == 'late' else '早退',
            'start': record.date.strftime('%Y-%m-%d'),
            'color': 'green' if record.status == 'attended' else 'red' if record.status == 'absent' else 'orange',
            'url': reverse('student_app:students_reportcomplete') + f'?date={record.date.strftime("%Y-%m-%d")}'  # URLを追加
        }
        for record in yearly_records
    ]

    context = {
        'monthly_stats': monthly_stats,
        'yearly_stats': yearly_stats,
        'calendar_data': calendar_data,  # カレンダーデータを追加
    }
    return render(request, 'attendance/attendance.html', context)

def calculate_attendance_stats(records):
    attended_days = records.filter(status='attended').count()
    absent_days = records.filter(status='absent').count()
    late_days = records.filter(status='late').count()
    early_leave_days = records.filter(status='early_leave').count()

    total_days = attended_days + absent_days
    attendance_rate = (attended_days / total_days * 100) if total_days > 0 else 0

    return {
        'attended_days': attended_days,
        'absent_days': absent_days,
        'late_days': late_days,
        'early_leave_days': early_leave_days,
        'attendance_rate': round(attendance_rate, 2)
    }