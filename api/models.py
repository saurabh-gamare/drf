from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    content = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)

    @property
    def sale_price(self):
        return '%.2f' % (float(self.price) * 0.8)


####TESTING PURPOSES
class Album(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100) 

    def __str__(self):
        return self.name


class Track(models.Model):
    name = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, 
                              related_name='album_data')
    
    def __str__(self):
        return self.name
