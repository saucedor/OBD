from django.urls import path
from OBD_users.views import *
from . import views 

urlpatterns = [
    path('', profile_view, name="profile"),
    path('edit/', profile_edit_view, name="profile-edit")
]