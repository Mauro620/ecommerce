from django.db import models

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    code = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.name

class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    code = models.CharField(max_length=10, null=False)
    country = models.ForeignKey(Country, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    postal_code = models.CharField(max_length=10, null=False)
    state = models.ForeignKey(State, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Address(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255, null=False)
    aditional_info = models.CharField(max_length=255, null=True, blank=True)
    city = models.ForeignKey(City, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.address}, {self.city.name}"