from django.shortcuts import render, redirect, get_object_or_404
from .models import Message
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def send_email(request):
    if request.method == "POST":
        recipient_name = request.POST.get('recipient')
        subject = request.POST.get('subject')
        body = request.POST.get('body')

        recipient_user = get_object_or_404(User, username=recipient_name)

 
        Message.objects.create(
            sender=request.user, 
            recipient=recipient_user,
            subject=subject,
            body=body
        )
        return redirect('inbox') 
    
    return render(request, 'post/send.html')

@login_required
def inbox(request):
    
    messages = Message.objects.filter(
        recipient=request.user, 
        is_archived=False, 
        is_deleted=False
    )
    return render(request, 'post/inbox.html', {'messages': messages, 'title': 'Входящие'})

@login_required
def sent_messages(request):
    messages = Message.objects.filter(sender=request.user)
    return render(request, 'post/inbox.html', {'messages': messages, 'title': 'Отправленные'})

@login_required
def detail_message(request, pk):
    message = get_object_or_404(Message, id=pk)

    if message.recipient == request.user and not message.is_read:
        message.is_read = True
        message.save() 

    return render(request, 'post/detail.html', {'message': message})

@login_required
def move_to_trash(request, pk):
    message = get_object_or_404(Message, id=pk, recipient=request.user)
    message.is_deleted = True 
    message.save()
    return redirect('inbox')

@login_required
def archive_message(request, pk):
    message = get_object_or_404(Message, id=pk, recipient=request.user)
    message.is_archived = True 
    message.save()
    return redirect('inbox')

@login_required
def delete_permanently(request, pk):
    message = get_object_or_404(Message, id=pk, recipient=request.user)
    message.delete() 
    return redirect('inbox')

# def index(request):
#     return render(request, 'post/index.html')