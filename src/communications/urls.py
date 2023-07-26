from django.urls import path

from . import views

urlpatterns = [
    path('themes/', views.ThemeListView.as_view(), name='theme-list'),
    path('themes/add', views.ThemeCreateView.as_view(), name='theme-create'),
    path('themes/<str:pk>', views.ThemeDetailView.as_view(), name='theme-detail'),

    path('messages/', views.MessageListView.as_view(), name='message-list'),
    path('messages/add', views.MessageCreateView.as_view(), name='message-create'),
    path('messages/<str:pk>', views.MessageDetailView.as_view(), name='message-detail'),
]
