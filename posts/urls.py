from django.urls import path
from . import views

app_name = "posts"

urlpattern = [
    path('create/', views.create, name="create"),
    
]