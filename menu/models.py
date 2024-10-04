from django.db import models
from django.urls import reverse, NoReverseMatch

NULLABLE = {'blank': True, 'null': True}


class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text='Уникальное имя меню')

    class Meta:
        verbose_name = "Имя"
        verbose_name_plural = "Имена"

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE, help_text='Название меню')
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, **NULLABLE)
    title = models.CharField(max_length=100, help_text='Название пункта меню')
    url = models.CharField(max_length=200, help_text='URL')
    order = models.PositiveIntegerField(default=0, help_text='Порядок отображения')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_url(self):
        try:
            return reverse(self.url)
        except NoReverseMatch:
            return self.url