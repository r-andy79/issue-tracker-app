from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('ticket/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/<int:pk>/comment', views.add_comment_to_ticket, name='add_comment_to_ticket'),
    path('ticket/new/', views.ticket_new, name='ticket_new'),
    path('accounts/logout/', views.logout, name='logout'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/registration/', views.registration, name='registration'),
    path('accounts/profile/', views.user_profile, name='profile'),
    path('ticket/<int:ticket_id>/user/<int:user_id>/vote', views.ticket_vote, name='ticket_vote')
]