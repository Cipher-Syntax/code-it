from django.urls import path
from . import views

urlpatterns = [
    path('create_posts/', views.create_posts_view, name='create_posts'),
    path('edit_posts/<uuid:posts_id>/', views.edit_posts_view, name='edit_posts'),
    path('delete/<uuid:post_id>/', views.delete_post_view, name='delete_post'),
    path('search/', views.search_view, name='search'),
]