# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Attendance(models.Model):
    # 'app.Student'を文字列で指定することで循環インポートを回避
    student = models.ForeignKey('app.Student', on_delete=models.CASCADE)  # 'app' は実際のアプリ名に変更
    attendance_time = models.DateTimeField(auto_now_add=True)

class Student(AbstractUser):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # パスワード用のフィールド
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    event_date = models.DateTimeField()  # 日付と開始時間を保存
    event_name = models.CharField(max_length=200)  # イベント名
    event_note = models.TextField(blank=True, null=True)  # 備考（任意）

    def __str__(self):
        return self.event_name
