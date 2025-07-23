from django.db import models
from django.contrib.auth.models import User
from customers.models import Profile
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Crop(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="crop_images/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="crops")

    def __str__(self):
        return self.name


class FarmerCrop(models.Model):
    farmer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="farmer_crops")
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="crop_listings")
    quantity = models.PositiveIntegerField(default=1)
    price_per_kg = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.farmer.user.username} - {self.crop.name} - ₹{self.price_per_kg}/kg"

