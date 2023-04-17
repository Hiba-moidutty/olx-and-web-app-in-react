from . import views
from django.urls import path


urlpatterns = [
    path('signup',views.signUp,name='signup'),
    path('user_login',views.user_login,name='user_login'),
    path('verify_token',views.verify_token,name='verify_token'),
    path('profile_view/<int:id>',views.profile_view,name='profile_view'),
    path('addImage/<int:id>',views.addImage,name='addImage'),

    #adminside
    path('admin_login',views.admin_login,name='admin_login'),
    path('user_list',views.user_list,name='user_list'),
    path('edit_user/<int:id>',views.edit_user,name='edit_user'),
    path('update_user/<int:id>',views.update_user,name='update_user'),
    # path('edit_user/<int:id>',views.edit_user,name='edit_user'),
    path('delete_user/<int:id>',views.delete_user,name='delete_user'),

]
