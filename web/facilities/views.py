from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.db import connection
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
import requests
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist


# 사용자 요청-결과값 넘겨주기 + 좋아요
@method_decorator(ensure_csrf_cookie, name='dispatch')
class InfoAPI(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        # 사용자 입력 받기
        facilities_type = request.data.get('facilities_type', '')
        lat = request.data.get('lat', '')
        lon = request.data.get('lon', '')
        radius = request.data.get('radius', '')

        # Flask 서버
        flask_server_url = 'http://127.0.0.1:5000/db_check'

    
        params = {
            "facilities_type": facilities_type,
            "lat": lat,
            "lon": lon,
            "radius": radius,

        }
        
        # Flask 서버에 입력받은 데이터 전송
        response = requests.get(flask_server_url, params)

        if response.status_code == 200:
            data = response.json()

            print(data)

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 주소에 좋아요
class LikeAPI(APIView):
    def post(self, request):
        username = request.data.get('username', '')
        liked = request.data.get('like', False)
        lat = request.data.get('lat', '')
        lon = request.data.get('lon', '')

        user = User.objects.get(email=username) 
        like_results = LikesResult.objects.filter(lat=lat, lon=lon, user=user)
        if like_results.exists():
            like_result = like_results.first()
            liked = like_result.like_state
            print(liked)
            like_result.like_state = not liked
            print(like_result.like_state)
            like_result.save()
        else:
            like_result = LikesResult.objects.create(lat=lat, lon=lon, like_state=True, user=user)

        response_data = {
            'liked': like_result.like_state,
            'lat': like_result.lat,
            'lon': like_result.lon,
            
        }

        return Response(response_data, status=status.HTTP_200_OK)


# 마이 페이지_좋아요 리스트 보여주기
class myLikeGETAPI(APIView):
    def post(self, request):
        username = request.data.get('username', '')
        try:
            user = User.objects.get(email=username)
            like_list = LikesResult.objects.filter(like_state=True, user=user)
            like_data = []

            for like_li in like_list:
                like_re = {
                    'like': like_li.like_state,
                    'lat': like_li.lat,
                    'lon': like_li.lon,
                }
                like_data.append(like_re)

            return Response(like_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)


# 마이페이지에서 2개 원룸 비교할 때 추가 사용자 입력
class extraInfo(APIView):
    def post(self, request):
        facilities_type = request.data.get('facilities_type', '')
        radius = request.data.get('radius', '')
        lat_1 = request.data.get('lat_1', '')
        lon_1 = request.data.get('lon_1', '')
        lat_2 = request.data.get('lat_2', '')
        lon_2 = request.data.get('lon_2', '')
    
        flask_server_url = 'http://127.0.0.1:5000//db_check_two'

        params = {
            "facilities_type":facilities_type,
            "radius":radius,
            "lat_1": lat_1,
            "lon_1": lon_1,
            "lat_2": lat_2,
            "lon_2": lon_2

        }

        response = requests.get(flask_server_url, params)

        if response.status_code == 200:
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



