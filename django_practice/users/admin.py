from django.contrib import admin

# Register your models here.
from .models import Profile,post_data,user_data,hostname

admin.site.register(Profile)
admin.site.register(post_data)
admin.site.register(user_data)
admin.site.register(hostname)