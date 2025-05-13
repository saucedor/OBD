from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

# Create your models here.

class Profile(models.Model):
    ROLE_CHOICES = (
        ('client', 'Cliente'),
        ('vendor', 'Vendor'),
    )
    role = models.CharField(max_length=7, choices=ROLE_CHOICES)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    displayname = models.CharField(max_length=20, null=True, blank=True)
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user)
    
    @property 
    def name(self):
        if self.displayname:
            name = self.displayname
        else:
            name = self.user.username
        return name
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('OBD/images/avatar.svg')
        return avatar 
        