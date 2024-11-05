from django.shortcuts import render
from django.shortcuts import render, redirect
from datetime import datetime
from .models import AttendanceRecord 
from app.models import Event

def students_event(request):
    return render(request, 'app/students_event.html')

def students_eventalert(request):
    return render(request, 'app/students_eventalert.html')
"""
# 生徒側への通知ページ
@login_required
def students_eventalert(request):

    # 管理者によるイベント削除の通知を取得
    notifications = EventDeletionNotification.objects.filter(student=request.user, seen=False)
    
    # 通知がある場合のみ通知ページを表示
    if notifications.exists():
        context = {'notifications': notifications}
        # 通知を表示済みに変更
        notifications.update(seen=True)
        return render(request, 'students/eventalert.html', context)
    else:
        return redirect('home')  # 通知がない場合はホームにリダイレクト
"""

def students_calendar(request):
    return render(request, 'app/students_calendar.html')

def students_report(request):
    return render(request, 'app/students_report.html')

def students_reportcomplete(request):
    return render(request, 'app/students_reportcomplete.html')

def students_admin_return(request):
    return render(request, 'app/students_admin_return.html')
"""
@login_required
def students_admin_return(request):
    # データが返却されたかどうかを確認
    data_returned = check_data_return_status()  # 管理者からの返却状況をチェックする関数
    
    if data_returned:
        # データが返却された場合のみ表示
        return render(request, 'students/admin_return.html')
    else:
        # 返却されていない場合はエラーページや別ページにリダイレクト
        return render(request, 'students/no_return.html')
"""

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

    context = {
        'monthly_stats': monthly_stats,
        'yearly_stats': yearly_stats
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

def student_event_list(request):
    events = Event.objects.all()  # すべてのイベントを取得
    return render(request, 'app/students_event.html', {'events': events})