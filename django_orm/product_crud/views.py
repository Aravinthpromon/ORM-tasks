import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ProductCategory, Product, Order


@csrf_exempt
def category_handler(request, category_id=None):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        category = ProductCategory.objects.create(name=name)
        
        return JsonResponse({
            "message": "Category created",
            "id": category.id,
            "name": category.name
        }, status=201)

    elif request.method == "PUT" and category_id:
        data = json.loads(request.body)
        category = get_object_or_404(ProductCategory, id=category_id)
        category.name = data.get("name", category.name)
        category.save()
        
        return JsonResponse({
            "message": "Category updated",
            "id": category.id,
            "name": category.name
        })

    elif request.method == "DELETE" and category_id:
        category = get_object_or_404(ProductCategory, id=category_id)
        category.delete()
        return JsonResponse({"message": "Category deleted"})

    elif request.method == "GET":
        if category_id:
            category = get_object_or_404(ProductCategory, id=category_id)
            # products = category.products.all().values( "name",)
            return JsonResponse({
                "id": category.id,
                "name": category.name,
                #  "products": list(products)
            })
        else:
            categories = ProductCategory.objects.all().values("id", "name")
            return JsonResponse(list(categories), safe=False)

    else:
        return JsonResponse({"error": "Invalid request"}, status=400)



@csrf_exempt
def product_handler(request, product_id=None):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        category_id = data.get("category_id")
        price = data.get("price")

        category = get_object_or_404(ProductCategory, id=category_id)
        product = Product.objects.create(name=name, category=category, price=price)

        return JsonResponse({
            "message": "Product created",
            "id": product.id,
            "name": product.name,
            "category_id": category.id,
            "category_name": category.name,
            "price": product.price
        },status=201)

    elif request.method == "PUT" and product_id:
        data = json.loads(request.body)
        product = get_object_or_404(Product, id=product_id)

        product.name = data.get("name", product.name)
        category_id = data.get("category_id", product.category.id)
        product.category = get_object_or_404(ProductCategory, id=category_id)
        product.price = data.get("price", product.price)

        product.save()

        return JsonResponse({
            "message": "Product updated",
            "id": product.id,
            "name": product.name,
            "category_id": product.category.id,
            "category_name": product.category.name,
            "price": product.price
        })

    elif request.method == "DELETE" and product_id:
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return JsonResponse({"message": "Product deleted"})

    elif request.method == "GET":
        if product_id:
            product = get_object_or_404(Product, id=product_id)
            return JsonResponse({
                "id": product.id,
                "name": product.name,
                "category_id": product.category.id,
                "category_name": product.category.name,
                "price": product.price
            })
        else:
            products = Product.objects.all().values("id", "name", "price", "category_id", "category__name")
            return JsonResponse(list(products), safe=False)

    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def order_handler(request, order_id=None):
    if request.method == "POST":
        data = json.loads(request.body)
        customer_name = data.get("customer_name")
        product_id = data.get("product_id")
        quantity = data.get("quantity")

        product = get_object_or_404(Product, id=product_id)
        order = Order.objects.create(customer_name=customer_name, product=product, quantity=quantity)

        return JsonResponse({
            "message": "Order created",
            "id": order.id,
            "customer_name": order.customer_name,
            "product_id": product.id,
            "product_name": product.name,
            "quantity": order.quantity,
            "cost": order.cost
        },status=201)

    elif request.method == "PUT" and order_id:
        data = json.loads(request.body)
        order = get_object_or_404(Order, id=order_id)

        order.customer_name = data.get("customer_name", order.customer_name)
        product_id = data.get("product_id", order.product.id)
        order.product = get_object_or_404(Product, id=product_id)
        order.quantity = data.get("quantity", order.quantity)

        order.save()

        return JsonResponse({
            "message": "Order updated",
            "id": order.id,
            "customer_name": order.customer_name,
            "product_id": order.product.id,
            "product_name": order.product.name,
            "quantity": order.quantity,
            "cost": order.cost
        })

    elif request.method == "DELETE" and order_id:
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        return JsonResponse({"message": "Order deleted"})

    elif request.method == "GET":
        if order_id:
            order = get_object_or_404(Order, id=order_id)
            return JsonResponse({
                "id": order.id,
                "customer_name": order.customer_name,
                "product_id": order.product.id,
                "product_name": order.product.name,
                "quantity": order.quantity,
                "cost": order.cost
            })
        else:
            orders = Order.objects.all().values("id", "customer_name", "product_id", "product__name", "quantity", "cost")
            return JsonResponse(list(orders), safe=False)

    else:
        return JsonResponse({"error": "Invalid request"}, status=400)
