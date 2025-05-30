from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static
from OBD_project import views


from . import views 

urlpatterns = [
    path("home/", views.home_view, name="home"),
    path("contacto/", views.contacto, name="contacto"),
    path("about/", views.about, name="about"),
]