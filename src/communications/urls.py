from django.urls import path

from . import views

urlpatterns = [
    path('themes/', views.ThemeListView.as_view(), name='theme-list'),
    path('themes/add', views.ThemeCreateView.as_view(), name='theme-create'),

    path('messages/', views.MessageListView.as_view(), name='message-list'),
    path('messages/add', views.MessageCreateView.as_view(), name='message-create'),

    path('comments/', views.CommentListView.as_view(), name='comment-list'),
    path('comments/add', views.CommentCreateView.as_view(), name='comment-create'),
]
