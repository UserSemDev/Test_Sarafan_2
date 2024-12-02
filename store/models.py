from django.db import models
from django.utils.text import slugify

from users.models import User

NULLABLE = {"null": True, "blank": True}


class Category(models.Model):
    """Категория товаров"""

    name = models.CharField(max_length=255, unique=True, verbose_name='Наименование категории')
    slug_name = models.SlugField(max_length=255, unique=True, **NULLABLE, verbose_name='Slug')
    image = models.ImageField(upload_to='store/categories/', verbose_name='Изображение')

    def save(self, *args, **kwargs):
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(models.Model):
    """Подкатегория товаров"""

    name = models.CharField(max_length=255, unique=True, verbose_name='Наименование подкатегории')
    slug_name = models.SlugField(max_length=255, unique=True, **NULLABLE, verbose_name='Slug')
    image = models.ImageField(upload_to='store/subcategories/', verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories',
                                 verbose_name='Категория')

    def save(self, *args, **kwargs):
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(models.Model):
    """Продукт"""

    name = models.CharField(max_length=255, unique=True, verbose_name='Наименование продукта')
    slug_name = models.SlugField(max_length=255, unique=True, **NULLABLE, verbose_name='Slug')
    image_small = models.ImageField(upload_to='store/products/small/', verbose_name='Изображение маленькое')
    image_medium = models.ImageField(upload_to='store/products/medium/', verbose_name='Изображение среднее')
    image_large = models.ImageField(upload_to='store/products/large/', verbose_name='Изображение большое')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products',
                                    verbose_name='Подкатегория')

    def save(self, *args, **kwargs):
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Cart(models.Model):
    """Корзина"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name='Пользователь')

    def clear(self):
        """Очистка корзины"""
        self.items.all().delete()

    def total_price(self):
        """Общая стоимость товаров в корзине"""
        return sum(item.total_price for item in self.items.all())

    def total_items(self):
        """Общее количество товаров в корзине"""
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"Корзина пользователя {self.user.name}"

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    """Элемент корзины"""
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, verbose_name='Корзина')
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    @property
    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name} в корзине {self.cart.user.name}"

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине '