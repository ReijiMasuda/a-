from django.urls import path
from .views import about, services, contact, faq

urlpatterns = [
    path('about/', about, name='about'),       # Aboutページ
    path('services/', services, name='services'),  # Servicesページ
    path('contact/', contact, name='contact'),      # Contactページ
    path('faq/', faq, name='faq'),                  # FAQページ
]
