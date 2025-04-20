from django.db import models
import uuid
from django.core.validators import RegexValidator, MinLengthValidator

class Users(models.Model):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    surname = models.CharField(max_length=50, null=False)
    phone_number = models.CharField(null=False, blank=False, max_length=15, 
        validators=[
            MinLengthValidator(7),
            RegexValidator(
                regex=r'^\d{7,15}$',
                message="Phone number must be between 7 and 15 digits.",
            )
        ]
    )
    password = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name