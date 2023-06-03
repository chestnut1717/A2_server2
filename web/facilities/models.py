from django.db import models
from accounts.models import *

class LikesResult(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    like_state = models.BooleanField(default=False, null=True)
    lat = models.CharField(max_length=100)
    lon = models.CharField(max_length=100)




    

    