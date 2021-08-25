from django.urls import path
from . import views

urlpatterns = [
    path("", views.starting_page, name = "starting-page-plain"),
    path('upl/', views.upload_files, name = 'upload_files'),
]