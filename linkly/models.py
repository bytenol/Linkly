from django.db import models


class LinklyUrl(models.Model):
    fromUrl = models.TextField(unique=True)
    toUrl = models.CharField(unique=True, max_length=10)
    expiration_date = models.DateTimeField(auto_now=True)
    last_visited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.toUrl