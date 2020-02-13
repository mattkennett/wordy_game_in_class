from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class WordyUser(AbstractUser):
    favorite_color = models.CharField(max_length=128, blank=True, null=True)
    score = models.IntegerField(default=0, blank=True, null=True)
