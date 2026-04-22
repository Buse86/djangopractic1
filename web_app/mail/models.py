from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)  # Входящие, Исходящие, Корзина, Архив
    

class EmailMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_emails', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_emails', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True)