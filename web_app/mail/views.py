from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import EmailMessage, Folder

@login_required
def send_email(request):
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        
        errors = {}
        if not recipient_username:
            errors['recipient'] = 'Укажите получателя'
        if not subject:
            errors['subject'] = 'Тема обязательна'
        if not body:
            errors['body'] = 'Текст письма обязателен'
        
        if errors:
            return render(request, 'mail/send_email.html', {'errors': errors})
        
        try:
            recipient = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            return render(request, 'mail/send_email.html', {'errors': {'recipient': 'Пользователь не найден'}})
        
        sender_folder, _ = Folder.objects.get_or_create(user=request.user, name='Исходящие')
        recipient_folder, _ = Folder.objects.get_or_create(user=recipient, name='Входящие')
        
        EmailMessage.objects.create(
            sender=request.user,
            recipient=recipient,
            subject=subject,
            body=body,
            folder=sender_folder,
            is_read=True  
        )
        
        EmailMessage.objects.create(
            sender=request.user,
            recipient=recipient,
            subject=subject,
            body=body,
            folder=recipient_folder,
            is_read=False
        )
        
        return redirect('email_list', folder_name='Исходящие')
    
    return render(request, 'mail/send_email.html')


@login_required
def email_list(request, folder_name):
    folder = get_object_or_404(Folder, user=request.user, name=folder_name)
    emails = EmailMessage.objects.filter(recipient=request.user, folder=folder).order_by('-sent_at')
    
    # Список папок для навигации
    folders = Folder.objects.filter(user=request.user)
    
    return render(request, 'mail/email_list.html', {
        'emails': emails,
        'folder': folder,
        'folders': folders,
    })


@login_required
def move_email(request, email_id):
    email = get_object_or_404(EmailMessage, id=email_id, recipient=request.user)
    new_folder_name = request.POST.get('folder')
    
    new_folder = get_object_or_404(Folder, user=request.user, name=new_folder_name)
    email.folder = new_folder
    email.save()
    
    return redirect('email_list', folder_name=new_folder_name)

@login_required
def view_email(request, email_id):
    email = get_object_or_404(EmailMessage, id=email_id, recipient=request.user)
    if not email.is_read:
        email.is_read = True
        email.save()
    return render(request, 'view_email.html', {'email': email})