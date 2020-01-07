from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('ticket/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/new/', views.ticket_new, name='ticket_new'),
    path('accounts/logout', views.logout, name='logout'),
    path('accounts/login', views.login, name='login')
]