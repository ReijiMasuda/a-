from django.db import models
from django.conf import settings
from django.contrib.auth.models import User  # Userモデルを使用する場合

class AttendanceRecord(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 生徒と関連付ける
    attendance_date = models.DateField()  # 出席日
    status = models.CharField(max_length=10, choices=[
        ('present', '出席'),
        ('absent', '欠席'),
        ('late', '遅刻'),
        ('early', '早退'),
    ])  # 出席状況

    def __str__(self):
        return f"{self.student} - {self.attendance_date} - {self.status}"
    
# イベント削除
class DeletedEvent(models.Model):
    date = models.DateField()
    time = models.TimeField()
    event_name = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_name