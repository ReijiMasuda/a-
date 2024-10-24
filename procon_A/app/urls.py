from django.urls import path
from .views import syusseki, students, event, alert
from . import views

urlpatterns = [
    path('syusseki/', syusseki, name='syusseki'),       # Aboutページ
    path('students/', views.student_list, name='student_list'),  # Servicesページ
    path('event/', event, name='event'),      # Contactページ
    path('alert/', alert, name='alert'),                  # FAQページ
    path('students/add_student/', views.add_student, name='add_student'),
]
