from django.contrib.auth.models import AbstractUser
from django.db import models

class AppUser(AbstractUser):
    email = models.EmailField(max_length=254)
