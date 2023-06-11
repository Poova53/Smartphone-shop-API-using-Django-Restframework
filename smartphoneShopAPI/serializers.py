from rest_framework import serializers
from .models import Product, ProductFeature, ProductImage, ProductReview, Cart


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'average_rating', 'ratings_count']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image_link']
        
class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ['feature']
        
class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['id', 'reviewer_name', 'summary', 'rating', 'verified_purchase', 'location', 'date', 'review']
        
class CartSerializer(serializers.ModelSerializer):
    class ProductNameSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ["name"]
    
    product = ProductNameSerializer(many=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    
    class Meta:
        model = Cart
        fields = ['id', 'product', 'no_of_items', 'total_price']
        
    def get_total_price(self, product: Product, cart: Cart):
        return product.price * cart.no_of_items
        
        
class ProductItemSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    product_feature = ProductFeatureSerializer(many=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'average_rating', 'ratings_count', 'product_image', 'product_feature']