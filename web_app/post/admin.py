from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipient', 'created_at', 'is_read')
    list_filter = ('is_read', 'is_archived', 'is_deleted')