from django.urls import include, path
from .views import *

app_name = "facilities"

urlpatterns = [
    path('info/', InfoAPI.as_view()),
    path('mylike/',myLikeGETAPI.as_view()),
    path('like/',LikeAPI.as_view()),
    path('extra/', extraInfo.as_view()),

    # path('like/', LikeResultAPI.as_view()),
]