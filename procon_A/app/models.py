# models.py
from django.db import models

class Student(models.Model):
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
