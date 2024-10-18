from django.urls import path
from .views import syusseki, students, event, alert

urlpatterns = [
    path('syusseki/', syusseki, name='syusseki'),       # Aboutページ
    path('students/', students, name='students'),  # Servicesページ
    path('event/', event, name='event'),      # Contactページ
    path('alert/', alert, name='alert'),                  # FAQページ
]
