from django.urls import path
from . import views
urlpatterns = [
    path('Ad/home',views.admin_home,name="admin_home"),
    path('Ad/new/admin', views.admin_register_page, name='admin_register_page'),
    path('Ad/new/admin/confirm', views.admin_register, name='admin_register'),
    path('Ad/user/management', views.user_management, name='user_management'),
    path('Ad/user/blog/display/<int:blog_id>', views.blog_display, name='admin_blog_display'),
    path('Ad/user/blog/delete/<int:id>', views.delete_post_confirm, name='admin_blog_delete_display'),
    path('Ad/user/blog/delete/confirm/<int:id>', views.delete_post, name='admin_blog_delete'),
    path('Ad/user/display/<int:id>', views.author_profile, name='admin_user_display'),
    path('Ad/user/remove/<int:id>', views.user_remove_confirm, name='admin_user_remove'),
    path('Ad/user/remove/confirm/<int:id>', views.user_remove, name='admin_user_remove_confirm')
]
