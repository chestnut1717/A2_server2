from ctypes import addressof
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=50,unique = True)
    email = models.CharField(max_length=50,unique = True, default='',null=False, blank=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    password = models.CharField(max_length=100)
    
class AddressResult(models.Model):
    addr_code = models.CharField(max_length=21)
    province_name = models.CharField(max_length=50)
    city_name = models.CharField(max_length=50)
    dong = models.CharField(max_length=50)


class Address(models.Model):
    code = models.CharField(db_column='Code', primary_key=True, max_length=21) 
    city = models.CharField(db_column='City', max_length=10, blank=True, null=True)  
    district = models.CharField(db_column='District', max_length=10, blank=True, null=True)  
    dong = models.CharField(db_column='Dong', max_length=10, blank=True, null=True)  

    class Meta:
        managed = True
        db_table = 'Address'



class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    addr_id  = models.ForeignKey(AddressResult, null=True, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    username_comment = models.CharField(max_length=100, null=True)
    input_addr = models.CharField(max_length=100)
    code_comment = models.CharField(max_length=100)

    def __str__(self):
        return self.content