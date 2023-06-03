from django.contrib import admin
from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    path('login/', loginAPI.as_view()),
    path('logout/', logout.as_view()),
    path('signup/', signup.as_view()),
    path('precomment/', precommentAPI.as_view()),
    path('comment/', AddrPostGetAPI.as_view()),
    path('mycomment/', mycommentAPI.as_view()),
] 