from rest_framework import serializers
from .models import *
from accounts.models import *

# class LikeResultSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=100)


# class InputSerializer(serializers.Serializer):
#     lat = serializers.CharField()
#     lon = serializers.CharField()

# class LikeSerializer(serializers.ModelSerializer):
#     liked = serializers.SerializerMethodField()
#     # like_count = serializers.ReadOnlyField()


#     class Meta:
#         model = likes
#         fields = '__all__'

#     def get_liked(self, obj):
#         user = self.context['request'].user
#         return user in obj.liked_users.all()