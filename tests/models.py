from django.db import models


class TestModel(models.Model):
    something = models.CharField(max_length=10)
    other = models.CharField(max_length=100)
