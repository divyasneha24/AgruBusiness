from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import FarmerCrop, Crop
import json
from django.views.decorators.csrf import csrf_exempt

from cart.models import OrderItem,Order
from customers.models import Profile
# Create your views here.

def farmer_home(request):
    farmer = request.user.profile  # Assuming `Profile` is linked to User

    # Get crops the farmer already owns
    owned_crops = FarmerCrop.objects.filter(farmer=farmer).values_list('crop_id', flat=True)

    # Get crops the farmer does NOT own
    available_crops = Crop.objects.exclude(id__in=owned_crops)

    # Get all crops the farmer is selling
    farmer_crops = FarmerCrop.objects.filter(farmer=farmer)

    if request.method == "POST":
        crop_id = request.POST.get('crop')
        quantity = request.POST.get('quantity')
        price_per_kg = request.POST.get('price_per_kg')

        if crop_id and price_per_kg:
            crop = Crop.objects.get(id=crop_id)
            FarmerCrop.objects.create(farmer=farmer, crop=crop, price_per_kg=price_per_kg,quantity=quantity)
            return redirect('farmer_home')  # Redirect to avoid resubmission

    return render(request, "F-home.html", {
        "farmer_crops": farmer_crops,
        "available_crops": available_crops  # Only crops the farmer doesn't have
    })

def update_price(request, crop_id):
    if request.method == "POST":
        data = json.loads(request.body)
        price = data.get('price_per_kg', 0)
        FarmerCrop.objects.filter(id=crop_id).update(price_per_kg=price)
        return JsonResponse({'status': 'success'})

def update_quantity(request, crop_id):
    if request.method == "POST":
        data = json.loads(request.body)
        quantity = data.get('quantity', 0)
        FarmerCrop.objects.filter(id=crop_id).update(quantity=quantity)
        return JsonResponse({'status': 'success'})

def toggle_availability(request, crop_id):
    if request.method == "POST":
        data = json.loads(request.body)
        is_available = data.get('is_available', False)
        FarmerCrop.objects.filter(id=crop_id).update(is_available=is_available)
        return JsonResponse({'status': 'success'})
    print("error")
    return JsonResponse({'status': 'error'})
    
def delete_crop(request, crop_id):
    if request.method == "POST":
        FarmerCrop.objects.filter(id=crop_id).delete()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})

def  orders(request):
    user = Profile.objects.get(user=request.user)

    if user.user_type == "customer":
        orders = Order.objects.filter(customer=request.user)
        
        if orders.exists():
            order_items = OrderItem.objects.filter(order__in=orders)
        else:
            print("orders doesn't exist")
            order_items = []  # Empty list if no orders exist

    else:
        orders =  Order.objects.filter(order_items__crop__farmer=user).distinct()
        order_items = OrderItem.objects.filter(crop__farmer=user).distinct()
    print(orders)
    print(order_items)
    return render(request, "orders.html" , {'orders':order_items,'user_type':user.user_type})

@csrf_exempt
def update_orderitem_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order_item_id = data.get("order_item_id")
            new_status = data.get("order_status")

            order_item = OrderItem.objects.get(id=order_item_id)
            order_item.order_status = new_status
            order_item.save()

            return JsonResponse({"success": True, "message": "Order item status updated."})
        except OrderItem.DoesNotExist:
            return JsonResponse({"success": False, "message": "Order item not found."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request."})