from rest_framework import viewsets, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from store.models import Category, Product, Cart, CartItem
from store.serializers import CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.prefetch_related('subcategories').all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.select_related('subcategory').all()
    serializer_class = ProductSerializer


class CartView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Добавление товара в корзину."""
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    def put(self, request, item_id):
        """Изменение количества товара в корзине."""
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in your cart"}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get('quantity')
        if quantity is None or int(quantity) < 1:
            return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity = int(quantity)
        cart_item.save()
        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        """Удаление товара из корзины."""
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.delete()
            return Response({"detail": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in your cart"}, status=status.HTTP_404_NOT_FOUND)


class ClearCartView(views.APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        """Полная очистка корзины."""
        try:
            cart = request.user.cart
            cart.clear()
            return Response({"detail": "Cart cleared successfully"}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error": "Cart does not exist"}, status=status.HTTP_404_NOT_FOUND)