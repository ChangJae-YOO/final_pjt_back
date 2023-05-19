from django.db import models
from django.conf import settings

# Create your models here.
class Query(models.Model):

    description = models.TextField()
    query = models.TextField()


class Theme(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    queries = models.ForeignKey(Query, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
