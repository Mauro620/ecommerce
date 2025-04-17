from django.db import models
import uuid

class Users(models.Model):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    surname = models.CharField(max_length=50, null=False)
    phone_number = models.IntegerField(null=False, blank=False)
    password = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name