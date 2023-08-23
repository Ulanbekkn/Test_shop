from django.contrib.auth.models import User
from django.db import models

from product.models import Product


class VerifyCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)

    def __str__(self):
        return self.code


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} favorite: {self.product.title}'

    class Meta:
        unique_together = ['user', 'product']


