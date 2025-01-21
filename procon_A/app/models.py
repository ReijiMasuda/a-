# models.py
from django.db import models
import datetime


class Attendance(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    attendance_time = models.DateTimeField(auto_now_add=True)

    # 出席状態: 〇 (出席), × (欠席), △ (遅刻)
    STATUS_CHOICES = [
        ('〇', '出席'),
        ('×', '欠席'),
        ('△', '遅刻'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='×')  # デフォルトは欠席

    def __str__(self):
        return f"{self.student.name} - {self.get_status_display()}"

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # パスワードフィールド
    registration_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.name


class Event(models.Model):
    event_date = models.DateTimeField()  # 日付と開始時間を保存
    event_name = models.CharField(max_length=200)  # イベント名
    event_note = models.TextField(blank=True, null=True)  # 備考（任意）

    def __str__(self):
        return self.event_name
