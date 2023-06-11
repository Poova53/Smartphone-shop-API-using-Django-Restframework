from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    asin_code = models.CharField(max_length=30)
    name = models.TextField()
    price = models.IntegerField()
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    ratings_count = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image_link = models.CharField(max_length=70)
    
    def __str__(self):
        return f"{self.product.name}'s image"

    class Meta:
        ordering = ['id']
    

class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_feature")
    feature = models.TextField()
    
    def __str__(self):
        return f"{self.product.name}'s feature"

    class Meta:
        ordering = ['id']
    
    
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_review")
    reviewer_name = models.CharField(max_length=50)
    summary = models.CharField(max_length=100, blank=True, null=True)
    rating = models.IntegerField()
    verified_purchase = models.BooleanField(default=False)
    location = models.CharField(max_length=30)
    date = models.DateField()
    review = models.TextField()
    
    class Meta:
        ordering = ['id']
    
    
class Cart(models.Model):
    user = models.ManyToManyField(User)
    product = models.ManyToManyField(Product, related_name="cart_product")
    no_of_items = models.IntegerField()


class Order(models.Model):
    
    YET_TO_DISPATCH = "Y"
    SHIPPED = "S"
    OUT_FOR_DELIVERY = "O"
    DELIVERED = "D"
    
    status_choice = (
        (YET_TO_DISPATCH, "Yet to dispatch"),
        (SHIPPED, "Shipped"),
        (OUT_FOR_DELIVERY, "Out for delivery"),
        (DELIVERED, "Delivered")
    )
    
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ordered_product")
    no_of_items = models.IntegerField()
    address = models.TextField()
    pincode = models.CharField(max_length=6)
    status = models.CharField(max_length=4, choices=status_choice, default=YET_TO_DISPATCH)
    ordered_time = models.DateTimeField(auto_now_add=True)
    
    

