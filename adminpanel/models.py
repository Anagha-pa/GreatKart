

# Create your models here.
from django.db import models
from django.db import models


# Create your models here.
class AdminLogin(models.Model):
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=50)   