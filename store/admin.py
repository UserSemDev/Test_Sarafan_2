from django.contrib import admin
from store.models import Category, Subcategory, Product, Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_items', 'total_price')
    search_fields = ('user__username',)
    inlines = [CartItemInline]

    def total_items(self, obj):
        return obj.total_items()

    def total_price(self, obj):
        return obj.total_price()

    total_items.short_description = "Total Items"
    total_price.short_description = "Total Price"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug_name')
    prepopulated_fields = {'slug_name': ('name',)}
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug_name', 'category')
    prepopulated_fields = {'slug_name': ('name',)}
    search_fields = ('name', 'category__name')
    list_filter = ('category',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug_name', 'subcategory', 'price', 'display_images')
    prepopulated_fields = {'slug_name': ('name',)}
    search_fields = ('name', 'subcategory__name', 'subcategory__category__name')
    list_filter = ('subcategory__category', 'subcategory')
    ordering = ('name',)

    def display_images(self, obj):
        if obj.image_small:
            return f"[Small] {obj.image_small.name}, [Medium] {obj.image_medium.name}, [Large] {obj.image_large.name}"
        return "No Images"

    display_images.short_description = "Product Images"