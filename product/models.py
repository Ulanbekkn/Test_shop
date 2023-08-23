from django.db import models


class Product(models.Model):
    image = models.ImageField('Фото', upload_to='Product_photo')
    title = models.CharField('Название', max_length=50)
    description = models.TextField('Описание')
    price = models.IntegerField('Цена')

    def __str__(self):
        return f'{self.id}: {self.title}, price:{self.price}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
