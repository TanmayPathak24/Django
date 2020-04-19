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
    path('Blog/author/signup', views.signup_page, name="author_signup_page"),
    path('Blog/author/signup/confirm', views.signup, name="author_signup"),
    path('Blog/author/signin', views.sign_in_page, name="author_login_page"),
    path('Blog/author/signin/confirm', views.signin, name="author_login"),
    path('Blog/author/logout', views.logout, name="author_logout"),
    path('Blog/search', views.search, name="blog_search"),
    path('Blog/author/display/<str:avatar>', views.blog_aulthor_display, name="blog_author_display"),
    path('Blog/author/blog/display', views.blog_aulthor_blog_display, name="blog_author_blog_display"),
    path('Blog/author/bio/update', views.author_update_page, name="blog_author_bio_update_page"),
    path('Blog/author/bio/update/confirm', views.author_bio_update, name="blog_author_bio_update")
]
