from django.urls import path
from . import views

urlpatterns = [
    path('',views.user_login,name='login'),
    path('signup/',views.user_signup,name='signup'),
    path('home/',views.user_home,name='home'),
    path('logout/',views.user_logout,name='logout'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('admin_user_edit/<id>',views.admin_user_edit,name='admin_user_edit'),
    path('admin_user_edit_post',views.admin_user_edit_post,name='admin_user_edit_post'),
    path('admin_add_user',views.admin_add_user,name='admin_add_user'),
    path('admin_delete_user/<id>',views.admin_delete_user,name='admin_delete_user')
]