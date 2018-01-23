from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return f'{self.name}'
