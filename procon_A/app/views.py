from django.shortcuts import render

def about(request):
    return render(request, 'app/about.html')  # Aboutページ

def services(request):
    return render(request, 'app/services.html')  # Servicesページ

def contact(request):
    return render(request, 'app/contact.html')  # Contactページ

def faq(request):
    return render(request, 'app/faq.html')  # FAQページ
