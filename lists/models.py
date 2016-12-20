from django.db import models


# nie usuwamy migracji, które były już zaaplikowane do bazy danych
# dobra praktyka - nie usuwamy migracji, które były już commitowane do gita


class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)
