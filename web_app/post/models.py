from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received")
    subject = models.CharField(max_length=200, verbose_name="Тема")
    body = models.TextField(verbose_name="Текст письма")
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} (от {self.sender})"