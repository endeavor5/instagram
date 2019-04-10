from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('create/', views.create, name="create"),
    path('', views.list, name="list"),
    path('<int:id>/update/', views.update, name="update"),
    path('<int:id>/delete/', views.delete, name="delete"),
]