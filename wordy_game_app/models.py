from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class WordyUser(AbstractUser):
    score = models.IntegerField(default=0, blank=True, null=True)