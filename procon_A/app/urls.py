from django.urls import path
from .views import syusseki, students, event, alert
from . import views
from .views import student_login, student_attendance

urlpatterns = [
    path('syusseki/', syusseki, name='syusseki'),       # Aboutページ
    path('students/', views.student_list, name='students'),  # Servicesページ
    path('student_login/', student_login, name='student_login'),  # 生徒ログインページ
    path('student/attendance/', student_attendance, name='student_attendance'),  # 出席ページ
    path('event/', views.event_list, name='event'),  # イベント一覧
    path('alert/', alert, name='alert'),                  # FAQページ
    path('students/add_student/', views.add_student, name='add_student'),
    path('event/add/', views.add_event, name='add_event'),  # イベント追加
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),  # イベント削除
]
