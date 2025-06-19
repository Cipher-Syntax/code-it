from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.landing_page_view, name='landing_page'),
    path('login/', views.login_view, name='login'),
    path('create_account/', views.create_account_view, name='create_account'),
    path('logout/', views.logout_view, name='logout'),
    path('posts_detail/<uuid:post_id>/', views.posts_details_view, name='posts_detail'),
    path('notification/', views.notification_view, name='notification'),
    path('notifications/mark_all_read/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
    path('notifications/read/<int:notification_id>/', views.read_notification, name='read_notification'),
    path('profile/<int:profile_id>/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('settings/', views.settings_view, name='settings'),
    path('toggle-like/', views.toggle_like, name='toggle_like'),
    path('toggle-comment-like/', views.toggle_comment_like, name='toggle_comment_like'),
    path('popular/', views.popular_view, name='popular_page'),
    path('hot/', views.hot_view, name='hot_page'),
    path('about/', views.about_us_view, name='about_us')
]
urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)