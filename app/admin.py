from django.contrib import admin
from .models import CartFood, Food, Restaurant, Category


admin.site.register(CartFood)
admin.site.register(Food)
admin.site.register(Restaurant)
admin.site.register(Category)
