from django.urls import path
from .views import (
    login_view,
    logout_view,
    profile_view,
    register_view
)
app_name = 'account'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name="register"),
    path('profile/', profile_view, name="profile"),
]
