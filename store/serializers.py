from rest_framework import serializers
from store.models import Subcategory, Category, Product, CartItem, Cart


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'slug_name', 'image']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug_name', 'image', 'subcategories']


class ProductSerializer(serializers.ModelSerializer):
    subcategory = serializers.SlugRelatedField(queryset=Subcategory.objects.all(), slug_field='slug_name')

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug_name', 'subcategory', 'price', 'image_small', 'image_medium', 'image_large']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_cost']

    def get_total_cost(self, obj):
        return sum(item.total_price for item in obj.items.all())

