from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class CustomizationCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Customization categories"

class CustomizationOption(models.Model):
    category = models.ForeignKey(CustomizationCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class ProductCustomization(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='customizations')
    customization_category = models.ForeignKey(CustomizationCategory, on_delete=models.CASCADE)
    default_option = models.ForeignKey(CustomizationOption, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('product', 'customization_category')

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart}"

class CartItemCustomization(models.Model):
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='customizations')
    customization_option = models.ForeignKey(CustomizationOption, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cart_item.product.name} - {self.customization_option.name}"