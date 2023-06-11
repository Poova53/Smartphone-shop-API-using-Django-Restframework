from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('products', views.products_list),
    path('products/<int:id>', views.product_detail),
    path('review/<int:id>', views.product_review),
    path('api-token-auth', obtain_auth_token),
    path('products/<int:id>/add-to-cart', views.add_to_cart),
    path('mycart', views.mycart),
    path('products/<int:id>/buy', views.buy_product),
]
