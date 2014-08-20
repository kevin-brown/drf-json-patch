from django.db import models


class TestModel(models.Model):
    something = models.CharField(max_length=100)
    other = models.CharField(max_length=100)


class FullNested(models.Model):
    name = models.CharField(max_length=100)


class ChildNested(models.Model):
    title = models.CharField(max_length=100)
    full = models.ManyToManyField(FullNested, related_name="children")
