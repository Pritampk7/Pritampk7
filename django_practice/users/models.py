from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None, created=False, **kwargs):
    if created:
        token = Token.objects.create(user=instance)

class post_data(models.Model):
    id = models.CharField(max_length=70, blank=False, default='', primary_key=True,null=False)
    data = models.CharField(max_length= 1000,blank=False, default='')


class user_data(models.Model):
    IP_address =models.GenericIPAddressField(max_length=16,blank=False,default="")
    username = models.CharField(max_length=15,blank=False,default="")
    password = models.CharField(max_length=20,blank=False,default="")
    device_type = models.CharField(max_length=20, blank=False,default="")

    def __str__(self):
        return self.IP_address

class hostname(models.Model):
    ip_address = models.ForeignKey(user_data,max_length=15,null=True,blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ip_address)

