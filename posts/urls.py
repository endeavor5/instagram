from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('create/', views.create, name="create"),
    path('', views.list, name="list"),
    path('<int:post_id>/update/', views.update, name="update"),
    path('<int:id>/delete/', views.delete, name="delete"),
    path('<int:post_id>/like/', views.like, name="like"),
    path('<int:post_id>/comment/create/', views.comment_create, name="comment_create"),
    path('<int:post_id>/comment/<int:comment_id>/delete/', views.comment_delete, name="comment_delete"),
]