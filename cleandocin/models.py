from django.db import models


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Document(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100, null=True)
    fmt = models.CharField(max_length=10, db_column='format', null=True)
    size = models.CharField(max_length=10, null=True)
    page_num = models.IntegerField(null=True)
    tag = models.ManyToManyField(Tag)
    valid = models.BooleanField(null=False)
    pending = models.BooleanField(default=False)