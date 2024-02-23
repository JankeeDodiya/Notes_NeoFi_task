from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('signup/', views.signup),
    path('notes/create/', views.note_create),
    path('notes/<int:pk>/', views.note_detail),
    path('notes/share/', views.share_note),
    path('notes/update/<int:pk>/', views.update_note),
    path('notes/version-history/<int:pk>/', views.version_history),
]
