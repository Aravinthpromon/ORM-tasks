import pytest
import base64
from django.urls import reverse
from rest_framework.test import APIClient
from product_crud.models import ProductCategory, Product, Order

# Set up test client with authentication
@pytest.fixture
def api_client():
    client = APIClient()
    credentials = "Basic " + base64.b64encode(b"admin:123").decode("utf-8")
    client.credentials(HTTP_AUTHORIZATION=credentials)  
    return client

@pytest.fixture
def product_category():
    return ProductCategory.objects.create(name="Electronics")

@pytest.fixture
def product(product_category):
    return Product.objects.create(name="Laptop", category=product_category, price=1000.00)

@pytest.fixture
def order(product):
    return Order.objects.create(customer_name="John Doe", product=product, quantity=2)

@pytest.mark.django_db
def test_create_category(api_client):
    """Test API: Create a new product category"""
    url = reverse('category_handler')
    response = api_client.post(url, {"name": "Books"}, format="json")
    # response = api_client.post(url, {}, format="json")

    assert response.status_code == 201
    assert response.json()["name"] == "Books"

@pytest.mark.django_db
def test_get_category(api_client, product_category):
    """Test API: Get an existing category"""
    url = reverse('category_detail', args=[product_category.id])
    # url = reverse('category_detail', args=[9])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.json()["name"] == product_category.name

@pytest.mark.django_db
def test_update_category(api_client, product_category):
    """Test API: Update a category"""
    url = reverse('category_detail', args=[product_category.id])
    response = api_client.put(url, {"name": "Updated Electronics"}, format="json")

    product_category.refresh_from_db()
    assert response.status_code == 200
    assert product_category.name == "Updated Electronics"

@pytest.mark.django_db
def test_delete_category(api_client, product_category):
    """Test API: Delete a category"""
    url = reverse('category_detail', args=[product_category.id])
    response = api_client.delete(url)

    assert response.status_code in [200, 201]  # Accepts both 200 and 201

    assert ProductCategory.objects.count() == 0


@pytest.mark.django_db
def test_create_product(api_client, product_category):
    """Test API: Create a new product"""
    url = reverse('product_handler')
    response = api_client.post(
        url, {"name": "Smartphone", "category_id": product_category.id, "price": 699.99}, format="json"
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Smartphone"
    # assert response.json()["price"] == "699.99"
    assert "{:.2f}".format(float(response.json()["price"])) == "{:.2f}".format(699.99)

@pytest.mark.django_db
def test_get_product(api_client, product):
    """Test API: Get an existing product"""
    url = reverse('product_detail', args=[product.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.json()["name"] == product.name
    # assert response.json()["price"] == str(product.price)
    assert "{:.2f}".format(float(response.json()["price"])) == "{:.2f}".format(product.price)


@pytest.mark.django_db
def test_update_product(api_client, product):
    """Test API: Update an existing product"""
    url = reverse('product_detail', args=[product.id])
    response = api_client.put(
        url, {"name": "Updated Laptop", "price": 1200.00, "category_id": product.category.id}, format="json"
    )

    product.refresh_from_db()
    assert response.status_code == 200
    assert product.name == "Updated Laptop"
    assert str(product.price) == "1200.00"

@pytest.mark.django_db
def test_delete_product(api_client, product):
    """Test API: Delete a product"""
    url = reverse('product_detail', args=[product.id])
    # url = reverse('product_detail', args=[9999])
    response = api_client.delete(url)

    assert response.status_code in [200, 204]  # Some APIs return 204 No Content
    assert Product.objects.count() == 0


@pytest.mark.django_db
def test_create_order(api_client, product):
    """Test API: Create an order and check automatic cost calculation"""
    url = reverse('order_handler')
    response = api_client.post(
        url, {"customer_name": "Jane Doe", "product_id": product.id, "quantity": 3}, format="json"
    )
    # url, {"customer_name": "Bob", "product_id": product.id, "quantity": -3}, format="json"  # Negative quantity
    # )

    assert response.status_code == 201
    assert response.json()["customer_name"] == "Jane Doe"
    assert response.json()["quantity"] == 3
    # assert response.json()["cost"] == str(product.price * 3)
    assert "{:.2f}".format(float(response.json()["cost"])) == "{:.2f}".format(product.price * 3) 

@pytest.mark.django_db
def test_get_order(api_client, order):
    """Test API: Get an existing order"""
    url = reverse('order_detail', args=[order.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.json()["customer_name"] == order.customer_name
    assert response.json()["quantity"] == order.quantity
    # assert response.json()["cost"] == str(order.cost)
    assert "{:.2f}".format(float(response.json()["cost"])) == "{:.2f}".format(order.cost)

@pytest.mark.django_db
def test_update_order(api_client, order, product):
    """Test API: Update an existing order"""
    url = reverse('order_detail', args=[order.id])
    response = api_client.put(
        url, {"customer_name": "Updated Name", "product_id": product.id, "quantity": 5}, format="json"
    )

    order.refresh_from_db()
    assert response.status_code == 200
    assert order.customer_name == "Updated Name"
    assert order.quantity == 5
    # assert str(order.cost) == str(product.price * 5)
    assert "{:.2f}".format(float(order.cost)) == "{:.2f}".format(product.price * 5)  

@pytest.mark.django_db
def test_delete_order(api_client, order):
    """Test API: Delete an order"""
    url = reverse('order_detail', args=[order.id])
    response = api_client.delete(url)

    assert response.status_code in [200, 204]
    assert Order.objects.count() == 0

