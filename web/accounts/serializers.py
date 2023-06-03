from rest_framework import serializers
from .models import *
from facilities.models import *


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password','username']



# 댓글 작성 및 조회
class CommentGetPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['username_comment', 'content','created_at']
        read_only_fields = ['id']

# 내가 작성한 목록 모아보기
class MyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['input_addr', 'content', 'created_at'] 
        read_only_fields = ['id']

