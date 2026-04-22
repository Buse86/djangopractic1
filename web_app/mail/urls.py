from django.urls import path
from . import views

urlpatterns = [
    path('', views.send_email, name='main_page'),
    path('send/', views.send_email, name='send_email'),
    path('list/<str:folder_name>/', views.email_list, name='email_list'),
    path('view/<int:email_id>/', views.view_email, name='view_email'),
    path('move/<int:email_id>/', views.move_email, name='move_email'),
]