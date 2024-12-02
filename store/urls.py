from django.urls import path
from rest_framework.routers import DefaultRouter

from store.apps import StoreConfig
from store.views import CategoryViewSet, ProductViewSet, CartView, CartItemView, ClearCartView

app_name = StoreConfig.name

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/item/', CartItemView.as_view(), name='cart-item'),
    path('cart/item/<int:item_id>/', CartItemView.as_view(), name='cart-item-detail'),
    path('cart/clear/', ClearCartView.as_view(), name='clear-cart'),
] + router.urls
