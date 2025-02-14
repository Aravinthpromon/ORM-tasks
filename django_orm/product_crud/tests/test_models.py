import pytest
from product_crud.models import ProductCategory, Product, Order

@pytest.mark.django_db
def test_create_category():
    """Test creating a product category"""
    category = ProductCategory.objects.create(name="Electronics")
    assert category.name == "Electronics"

@pytest.mark.django_db
def test_create_product():
    """Test creating a product and verifying its details"""
    category = ProductCategory.objects.create(name="Electronics")
    product = Product.objects.create(name="Smartphone", category=category, price=60000.00)
    
    assert product.name == "Smartphone"
    assert product.price == 60000.00
    assert product.category.name == "Electronics"

@pytest.mark.django_db
def test_create_order():
    """Test order creation and automatic cost calculation"""
    category = ProductCategory.objects.create(name="Electronics")
    product = Product.objects.create(name="Laptop", category=category, price=85000.00)
    order = Order.objects.create(customer_name="Alice", product=product, quantity=2)

    assert order.customer_name == "Alice"
    assert order.quantity == 2
    assert order.cost == product.price * order.quantity  # Order cost should be auto-calculated
