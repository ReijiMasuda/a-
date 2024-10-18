from django.shortcuts import render

def syusseki(request):
    return render(request, 'app/syusseki.html')  # Aboutページ

def students(request):
    return render(request, 'app/students.html')  # Servicesページ

def event(request):
    return render(request, 'app/event.html')  # Contactページ

def alert(request):
    return render(request, 'app/aler.html')  # FAQページ
