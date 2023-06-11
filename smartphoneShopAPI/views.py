from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from .models import Product, ProductFeature, ProductImage, ProductReview, Cart, Order
from .serializers import ProductSerializer, ProductImageSerializer, ProductFeatureSerializer, ProductReviewSerializer, ProductItemSerializer
from .serializers import CartSerializer
from django.core.paginator import Paginator, EmptyPage
from rest_framework.request import Request
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(["GET"])
def products_list(request: Request):
    items = Product.objects.all()
    
    page = request.query_params.get('page', default=1)
    brand = request.query_params.get('brand')
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')
    ratings = request.query_params.get('ratings')
    
    if brand:
        items = items.filter(name__icontains=brand)
    if min_price:
        items = items.filter(price__gte=min_price)
    if max_price:
        items = items.filter(price__lte=max_price)
    if ratings:
        ratings = round(float(ratings), 1)
        if ratings <= 5 and ratings >= 0:
            items = items.filter(average_rating__gte=ratings)
        
    total_items = len(items)
    
    paginator = Paginator(items, 10)
    
    try:
        items = paginator.page(number=page)
    except EmptyPage:
        items = []
        
    serialized_item = ProductSerializer(items, many=True)
    
    return Response({
                        'status': "success",
                        "Search result": f"Found {total_items} products",
                        "products": serialized_item.data,
                        },
                    status=status.HTTP_200_OK)


@api_view(["GET"])
def product_detail(request: Request, id):
    product = get_object_or_404(Product.objects.prefetch_related('product_image', 'product_feature'), pk=id)
    
    serialized_item = ProductItemSerializer(product)
    
    return Response({"status": "success", "data":serialized_item.data}, status=status.HTTP_200_OK)
    
    
@api_view(["GET"])
def product_review(request: Request, id):
    product = get_object_or_404(Product.objects.prefetch_related("product_review"), pk=id)
    
    reviews = product.product_review.all()
    
    page_no = request.query_params.get('page_no', default=1)
    sort_by = request.query_params.get('sort_by')
    
    if sort_by:
        if sort_by.lower() == "highest":
            reviews = reviews.order_by('-rating')
        elif sort_by.lower() == "lowest":
            reviews = reviews.order_by('rating')
        elif sort_by.lower() == "newest":
            reviews = reviews.order_by('-date')
    
    paginator = Paginator(reviews, 5)
    
    try:
        items = paginator.page(page_no)
    except EmptyPage:
        items = []
        
    serialized_product = ProductSerializer(product)
    serialized_review = ProductReviewSerializer(items, many=True)
    
    return Response(
        {
            "status": "success",
            "product": serialized_product.data,
            "reviews": serialized_review.data
        },
        status=status.HTTP_200_OK
    )
    

@api_view(['POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated]) 
def add_to_cart(request: Request, id):
    product = get_object_or_404(Product, pk=id)
    no_of_items = int(request.data['no_of_items'])
    
    cart = Cart.objects.filter(product=product, user=request.user)
    
    if request.method == "POST":
        if cart:
            return Response(
                {
                    "status": "error",
                    "message": "cart already exist. Use put or delete to change number of items or delete the cart"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
                    
        new_cart = Cart.objects.create(no_of_items= no_of_items)
        new_cart.save()
        new_cart.product.add(product)
        new_cart.user.add(request.user)
    
        return Response(
                        {
                            'status': "success", 
                            "message": "items added to cart",
                            "detail": {
                                "product": product.name,
                                "price": product.price,
                                "no_of_items": new_cart.no_of_items,
                                "total_price": product.price * new_cart.no_of_items
                            },
                        }, 
                        status.HTTP_201_CREATED
                        )
    
    if not cart:
        return Response(
            {
                "status": "error",
                "message": "Need product in the cart to perform this method"
             },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    if request.method == "PUT":
        cart[0].no_of_items = no_of_items
        cart[0].save()
        
        return Response(
            {
                "status": "success",
                "message": "number of items changed successfully"
            },
            status=status.HTTP_200_OK
                        )
    
    if request.method == "DELETE":
        cart.delete()
        return Response(
            {
                "status": "success",
                "message": "Item removed from the cart successfully"
            },
            status=status.HTTP_200_OK
        )
        
        
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def mycart(request: Request):
    carts = Cart.objects.filter(user=request.user)
    
    if not carts:
        return Response(
            {
                "status": "Cart not available",
                "message": "Please add some items to the cart to view carts"
            },
            status.HTTP_204_NO_CONTENT
        )
        
    if request.method == "DELETE":
        carts.delete()
        
        return Response(
            {
                "status": "success",
                "message": "Cart items removed successfully"
            },
            status=status.HTTP_200_OK
        )
    
    cart_details = []
    
    for item in carts:
        product = item.product.all()[0]
        
        temp_dic = {
            "product id": product.id,
            "product name": product.name,
            "number of items": item.no_of_items,
            "total price": item.no_of_items * product.price
        }
        
        cart_details.append(temp_dic)
        
    total_amount = sum([i["total price"] for i in cart_details])
        
    
    return Response(
        {
            'status': 'success',
            'total amount': total_amount,
            'cart details': cart_details
        },
        status.HTTP_200_OK
    )
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_product(request: Request, id):
    product = get_object_or_404(Product, pk=id)
    
    no_of_items = request.data.get("no_of_items", None)
    address = request.data.get("address", None)
    pincode = request.data.get("pincode", None)
    
    if None in [no_of_items, address, pincode] or not no_of_items.isnumeric() or not pincode.isnumeric():
        return Response({"status": "form error", "message": "Invalid form data"}, status.HTTP_400_BAD_REQUEST)
    
    new_order = Order.objects.create(ordered_by=request.user, product=product, no_of_items=int(no_of_items), address=address, pincode=pincode)
    new_order.save()
    
    return Response({"status":"success", "message":"Product ordered successfully", "order id":new_order.pk}, status.HTTP_200_OK)