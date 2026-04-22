from django.urls import path
from . import views
from django.views.generic import RedirectView 

urlpatterns = [
    path('', RedirectView.as_view(url='inbox/')), 
    
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent_messages, name='sent'),
    path('send/', views.send_email, name='send_email'),
    path('message/<int:pk>/', views.detail_message, name='detail_message'),
    
    path('message/<int:pk>/trash/', views.move_to_trash, name='move_to_trash'),
    path('message/<int:pk>/archive/', views.archive_message, name='archive_message'),
    path('message/<int:pk>/delete/', views.delete_permanently, name='delete_permanently'),
]