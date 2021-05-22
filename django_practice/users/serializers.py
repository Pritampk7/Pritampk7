from rest_framework import serializers
from .models import post_data

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = post_data
        fields = ('id',
                  'data')

