from django.urls import path

from . import views

urlpatterns = [
    path('main/', views.main_view, name='main-view'),
    path('main/upload/', views.file_upload_view, name='upload-view'),
]
