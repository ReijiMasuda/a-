from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import StudentAddForm
from .models import Student

def syusseki(request):
    return render(request, 'app/syusseki.html')  # Aboutページ

def students(request):
    return render(request, 'app/students.html')  # Servicesページ

def event(request):
    return render(request, 'app/event.html')  # Contactページ

def alert(request):
    return render(request, 'app/alert.html')  # FAQページ


def add_student(request):
    if request.method == 'POST':
        form = StudentAddForm(request.POST)
        if form.is_valid():
            form.save()  # データベースに生徒情報を保存
            return redirect('student_list')  # 生徒一覧ページなどにリダイレクト
    else:
        form = StudentAddForm()

    return render(request, 'app/students_add.html', {'form': form})

def student_list(request):
    # データベースから全ての生徒を取得
    students = Student.objects.all()
    return render(request, 'app/students.html', {'students': students})