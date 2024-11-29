from django.urls import path
from .views import students_admin_return, students_calendar, students_eventalert, students_report, students_reportcomplete
from . import views

app_name = 'student_app'

urlpatterns = [
    path('event/', views.student_event_list, name='students_event'),
    path('eventalert/', students_eventalert, name='students_eventalert'),
    #path('eventalert/', staff_member_required(students_eventalert), name='students_eventalert'),
    path('calendar/', students_calendar, name='students_calendar'),
    path('report/', students_report, name='students_report'),
    path('reportcomplete/', students_reportcomplete, name='students_reportcomplete'),
    path('adminreturn/', students_admin_return, name='students_admin_return'),
    #path('adminreturn/', login_required(students_admin_return), name='students_admin_return'),
]