from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib import auth
from .serializers import LoginSerializer, SignupSerializer
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from facilities.models import *
from django.db import models
from django.db.models import Count

# 로그인
@method_decorator(ensure_csrf_cookie, name='dispatch')
class loginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = auth.authenticate(
                request=request,
                email=serializer.data['email'],
                password=serializer.data['password']
            )
            if user is not None:
                auth.login(request, user)
                response = JsonResponse({'message': '로그인 되었습니다.'})
                response.set_cookie('sessionid', request.session.session_key)
                return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 회원가입
class signup(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save(password = make_password(serializer.validated_data['password']))
            return Response({"user" : serializer.data['username'], "email":serializer.data['email']},status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

# 로그아웃
class logout(APIView):
    def get(self, request):
        auth.logout(request)
        return Response({'message':'로그아웃 완료'},status=status.HTTP_200_OK)
    

# 리뷰 작성
class AddrPostGetAPI(APIView):
    def post(self, request):
        username = request.data.get('username', '')
        province = request.data.get('province', '')
        district = request.data.get('district','')
        dong = request.data.get('dong', '')
        content = request.data.get('content', '')
        input_addr = request.data.get('addr', '')

        user = User.objects.get(email=username)

        existing_address_result = AddressResult.objects.filter(province_name=province, city_name=district, dong=dong)

        if existing_address_result.exists():
            # 이미 해당 province, city, dong 값이 있는 경우
            address_result = existing_address_result.first()

            comment = Comment.objects.create(
                username_comment=user,
                addr_id=address_result,
                content=content,
                input_addr=input_addr,
                code_comment=address_result.addr_code,
            )

            all_comment = Comment.objects.filter(code_comment = address_result.addr_code)
            serializer = CommentGetPostSerializer(all_comment, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            address = Address.objects.filter(city=province, district=city, dong=dong)

            if address.exists():
                address_result = AddressResult.objects.create(
                    addr_code=address.first().code,
                    province_name=province,
                    city_name=city,
                    dong=dong,
                )

                comment = Comment.objects.create(
                    username_comment=user,
                    addr_id=address_result,
                    content=content,
                    input_addr=input_addr,
                    code_comment=address_result.addr_code,
                )

                all_comment = Comment.objects.filter(code_comment = address_result.addr_code)
                serializer = CommentGetPostSerializer(all_comment, many=True)


                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)


# post - 이전에 작성한 리뷰들 모두 보여주기
class precommentAPI(APIView):
    def post(self, request):
        province = request.data.get('province', '')
        city = request.data.get('city', '')
        dong = request.data.get('dong', '')

        old_addr = AddressResult.objects.filter(province_name=province, city_name=city, dong=dong) 
        addr_codes = old_addr.values_list('addr_code', flat=True) 
        all_comment = Comment.objects.filter(code_comment__in=addr_codes)
        serializer = CommentGetPostSerializer(all_comment, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



# 마이페이지_작성한 리뷰 목록
class mycommentAPI(APIView):
    def post(self, request):
        username = request.data.get('username', '')
        user = User.objects.get(email=username)
        my_comments = Comment.objects.filter(username_comment = user)
        serializer = MyCommentSerializer(my_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



