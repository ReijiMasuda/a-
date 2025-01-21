# forms.py
from django import forms
from .models import Student

class StudentAddForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ['name', 'student_id', 'email', 'password', 'registration_date']


