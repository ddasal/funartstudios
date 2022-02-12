from django.urls import path

from .views import (
    profile_update_view,
    login_view,
    logout_view,
    change_password_view,
    register_view,
    account_list_view,
    profile_admin_update_view
)
app_name = 'account'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name="register"),
    path('change-password/', change_password_view, name="change-password"),
    path('profile/', profile_update_view, name="profile"),
    path('profile/<int:id>/', profile_admin_update_view, name="profile-admin-edit"),
    path('staff/', account_list_view, name="staff"),
]
