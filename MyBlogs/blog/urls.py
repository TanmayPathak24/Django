from django.urls import path
from . import views
from .forms import BlogForm
urlpatterns = [
    path('', views.home, name="blog_home"),
    path('about/', views.about, name="blog_about"),
    path('Blog/newBlog/', views.new_blog_page, name="blog_new_blog"),
    path('Blog/new_blog_entry/', views.new_blog, name="blog_new_blog_entry"),
    path('Blog/update_page/<int:blog_id>', views.blog_update_page, name="blog_update_page"),
    path('Blog/update/<int:blog_id>', views.blog_update, name="blog_update"),
    path('Blog/delete/<int:blog_id>', views.delete_confirmation_page, name="blog_delete_confirmation"),
    path('Blog/delete/confirm/<int:blog_id>', views.delete_post, name="blog_delete"),
    path('Blog/display/<int:blog_id>', views.display_post, name="blog_display"),
]
