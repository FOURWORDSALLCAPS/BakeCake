from django.utils import timezone
from django.db import models


class Cake(models.Model):
    name = models.CharField('Название торта', max_length=50, db_index=True, blank=True)
    created_at = models.DateTimeField('Когда создано объявление', default=timezone.now, db_index=True)
    price = models.IntegerField('Цена торта', db_index=True)
    comment = models.TextField('Комментарий к заказу', blank=True)
    form = models.CharField('Форма торта', max_length=50)
    quantity_levels = models.IntegerField('Количество уровней торта', db_index=True)
    topping = models.CharField('Топпинг торта', max_length=50)
    berries = models.CharField('Ягоды в торте', max_length=50, blank=True)
    decor = models.CharField('Декор торта', max_length=50, blank=True)
    inscription = models.CharField('Надпись на  торт', max_length=50, blank=True)
    delivery_address = models.CharField('Адрес доставки', max_length=100)
    delivery_date = models.DateTimeField('Время доставки', default=timezone.now, db_index=True)
    image = models.ImageField('Картинка', upload_to='cake', blank=True)

    def __str__(self):
        return f"{self.name} ({self.price}р.)"


class AboutUs(models.Model):
    telegram = models.CharField('Telegram компании', max_length=200, db_index=True)
    instagram = models.CharField('Instagram компании', max_length=200, db_index=True)
    phone_number = models.CharField('Номер компании', max_length=20, db_index=True)
    address = models.CharField('Адрес компании', max_length=200, db_index=True)

    def __str__(self):
        return self.telegram
