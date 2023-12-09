from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images', blank=True)


    class Meta:
        verbose_name_plural = 'Categories'


    def __str__(self):
        return self.title
    

class Restaurant(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to='images', blank=True)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name
    

class Food(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=250)
    price = models.IntegerField()
    categories = models.ManyToManyField(Category, blank=True)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return f'{self.name} from {self.restaurant}'


class CartFood(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.food}"
