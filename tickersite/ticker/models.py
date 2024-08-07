from django.db import models

# Create your models here.
class Query(models.Model):
    query_text = models.CharField(max_length=200)

    def __str__(self):
        return self.query_text