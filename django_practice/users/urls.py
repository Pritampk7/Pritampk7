from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/post-data/backend/primary$', views.data_posted_form_one),
    url(r'^api/post-data/backend/secondary$', views.data_posted_form_two),
    url(r'^api/post-data/backend/secondary$', views.post_ips)
]