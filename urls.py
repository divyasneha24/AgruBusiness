from django.urls import path
from . import views

urlpatterns = [
    path('farmer_home/', views.farmer_home, name='farmer_home'),
    path('update_price/<int:crop_id>/', views.update_price, name='update_price'),
    path('update_quantity/<int:crop_id>/', views.update_quantity, name='update_quantity'),
    path('toggle_availability/<int:crop_id>/', views.toggle_availability, name='toggle_availability'),
    path('delete_crop/<int:crop_id>/', views.delete_crop, name='delete_crop'),
    path('orders/', views.orders, name='orders'),
    path("update-orderitem-status/", views.update_orderitem_status, name="update_orderitem_status"),

]
