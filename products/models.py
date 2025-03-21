from django.db import models

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('gym_equipment', 'Gym Equipment'),
        ('clothing', 'Clothing'),
        ('shoes', 'Shoes'),
        ('supplements', 'Supplements'),
        ('sports_gear', 'Sports Gear'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name


