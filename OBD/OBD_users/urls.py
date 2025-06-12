from django.urls import path
from OBD_users.views import *
from . import views 

urlpatterns = [
    path('', profile_view, name="profile"),
    path('edit/', profile_edit_view, name="profile-edit"),
    path('onboarding/', profile_edit_view, name="profile-onboarding"),
    path('settings/', profile_settings_view, name="profile-settings"),
    path('emailchange/', profile_emailchange, name="profile-emailchange"),
    path('emailverify/', profile_emailverify, name="profile-emailverify"),
    path('delete/', profile_delete_view, name="profile-delete"),
    path('users/', views.users_list, name="users-list"),
    path("users/<int:pk>/", views.detalle_usuario, name="detalle_usuario"),
    path("users/<int:pk>/editar/", views.editar_usuario, name="editar_usuario"),
]