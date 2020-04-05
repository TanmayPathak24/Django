from django.urls import path
from . import views
urlpatterns = [
    path('Ad/home',views.admin_home,name="admin_home"),
    path('Ad/new/admin', views.admin_register_page, name='admin_register_page'),
    path('Ad/new/admin/confirm', views.admin_register, name='admin_register')
]
