from django.contrib import admin

from .models import FarmerCrop, Crop, Category

admin.site.register(Category)
admin.site.register(Crop)
admin.site.register(FarmerCrop)