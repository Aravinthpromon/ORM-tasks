from django.db import models

class ProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "product_category"  # Custom table name

    def __str__(self):
        return f"Category {self.id}: {self.name}"


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "product"  # Custom table name

    def __str__(self):
        return f"Product {self.id}: {self.name} ({self.category.name})"


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    quantity = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "order"  # Custom table name

    def save(self, *args, **kwargs):
        self.cost = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"
