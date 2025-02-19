from django.urls import path
from .views import syusseki, students, event, alert
from . import views
from .views import student_login, student_attendance
from .views import student_login

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
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/edit/<int:student_id>/', views.edit_student, name='edit_student'),  # 生徒編集のURL
    path('syusseki/', views.syusseki, name='syusseki'),
    path('attendance/edit/<int:student_id>/', views.edit_attendance, name='edit_attendance'),

]
