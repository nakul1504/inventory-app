from datetime import datetime
from decimal import Decimal

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from bson import ObjectId, Decimal128
from .forms import ProductForm, SupplierForm, SaleOrderForm, StockMovementForm
from inventory_management.settings import db


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')
class AddProductView(View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'add_product.html', {'form': form})

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            price = form.cleaned_data['price']
            stock_quantity = form.cleaned_data['stock_quantity']
            supplier_id = form.cleaned_data['supplier']

            if db.products.find_one({"name": name}):
                return HttpResponse("Product already exists", status=400)

            supplier = db.suppliers.find_one({"_id": ObjectId(supplier_id)})
            if not supplier:
                return HttpResponse("Invalid supplier", status=400)

            supplier_name = supplier['name']



            db.products.insert_one({
                'name': name,
                'description': description,
                'category': category,
                'price': Decimal128(str(price)),
                'stock_quantity': stock_quantity,
                'supplier': supplier_name
            })
            return redirect('product-list')

        return render(request, 'add_product.html', {'form': form})


class ProductListView(View):
    def get(self, request):
        products = db.products.find()
        return render(request, 'product_list.html', {'products': products})


class AddSupplierView(View):
    def get(self, request):
        form = SupplierForm()
        return render(request, 'add_supplier.html', {'form': form})

    def post(self, request):
        form = SupplierForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']

            if db.suppliers.find_one({"email": email}):
                return HttpResponse("Supplier already exists", status=400)

            db.suppliers.insert_one({
                'name': name,
                'email': email,
                'phone': phone,
                'address': address
            })
            return redirect('supplier-list')

        return render(request, 'add_supplier.html', {'form': form})


class SupplierListView(View):
    def get(self, request):
        suppliers = db.suppliers.find()
        return render(request, 'supplier_list.html', {'suppliers': suppliers})

class AddStockMovementView(View):
    def get(self, request):
        form = StockMovementForm()
        return render(request, 'add_stock_movement.html', {'form': form})

    def post(self, request):
        form = StockMovementForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            movement_type = form.cleaned_data['movement_type']
            notes = form.cleaned_data['notes']

            product = db.products.find_one({"_id": ObjectId(product_id)})
            if not product:
                return HttpResponse("Product not found", status=404)

            if movement_type == 'In':
                new_stock = product['stock_quantity'] + quantity
            elif movement_type == 'Out':
                if product['stock_quantity'] < quantity:
                    return HttpResponse("Not enough stock", status=400)
                new_stock = product['stock_quantity'] - quantity

            db.stock_movements.insert_one({
                'product_id': ObjectId(product_id),
                'quantity': quantity,
                'movement_type': movement_type,
                'notes': notes,
            })

            db.products.update_one(
                {"_id": ObjectId(product_id)},
                {"$set": {"stock_quantity": new_stock}}
            )
            return redirect('stock-level-check')

        return render(request, 'add_stock_movement.html', {'form': form})

class CreateSaleOrderView(View):
    def get(self, request):
        form = SaleOrderForm()
        return render(request, 'create_sale_order.html', {'form': form})

    def post(self, request):
        form = SaleOrderForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']

            product = db.products.find_one({"_id": ObjectId(product_id)})
            if product['stock_quantity'] < quantity:
                return HttpResponse("Insufficient stock", status=400)

            price = Decimal(product['price'].to_decimal())
            total_price = price * quantity

            db.sale_orders.insert_one({
                'product_id': ObjectId(product_id),
                'product_name': product['name'],
                'quantity': quantity,
                'total_price': Decimal128(total_price),
                'sale_date': datetime.now(),
                'status': 'Pending'
            })

            db.products.update_one({"_id": ObjectId(product_id)}, {"$set": {"stock_quantity": product['stock_quantity'] - quantity}})
            return redirect('sale-order-list')

        return render(request, 'create_sale_order.html', {'form': form})

class CancelSaleOrderView(View):

    def get(self, request, sale_order_id):
        sale_order = db.sale_orders.find_one({"_id": ObjectId(sale_order_id)})
        if not sale_order:
            return HttpResponse("Sale order not found", status=404)

        return render(request, 'cancel_sale_order.html', {'sale_order': sale_order})

    def post(self, request, sale_order_id):
        sale_order = db.sale_orders.find_one({"_id": ObjectId(sale_order_id)})
        if not sale_order:
            return HttpResponse("Sale order not found", status=404)

        if sale_order['status'] == 'Completed':
            return HttpResponse("Sale order already completed", status=400)

        db.sale_orders.update_one({"_id": ObjectId(sale_order_id)}, {"$set": {"status": "Cancelled"}})

        product = db.products.find_one({"_id": sale_order['product_id']})
        new_stock_quantity = product['stock_quantity'] + sale_order['quantity']
        db.products.update_one({"_id": sale_order['product_id']}, {"$set": {"stock_quantity": new_stock_quantity}})

        return redirect('sale-order-list')


class CompleteSaleOrderView(View):

    def get(self, request, sale_order_id):
        sale_order = db.sale_orders.find_one({"_id": ObjectId(sale_order_id)})
        if not sale_order:
            return HttpResponse("Sale order not found", status=404)

        return render(request, 'complete_sale_order.html', {'sale_order': sale_order})


    def post(self, request, sale_order_id):
        sale_order = db.sale_orders.find_one({"_id": ObjectId(sale_order_id)})
        if not sale_order:
            return HttpResponse("Sale order not found", status=404)

        if sale_order['status'] != 'Pending':
            return HttpResponse("Sale order cannot be completed", status=400)

        db.sale_orders.update_one({"_id": ObjectId(sale_order_id)}, {"$set": {"status": "Completed"}})

        return redirect('sale-order-list')

class SaleOrderListView(View):
    def get(self, request):
        sale_orders = db.sale_orders.find()
        sale_orders_list = [
            {
                'id': str(order['_id']),
                'product_id': str(order['product_id']),
                'product_name': order['product_name'],
                'quantity': order['quantity'],
                'total_price': float(order['total_price'].to_decimal()),
                'sale_date': order['sale_date'].strftime('%Y-%m-%d %H:%M:%S'),
                'status': order['status'],
            }
            for order in sale_orders
        ]
        return render(request, 'sale_order_list.html', {'sale_orders': sale_orders_list})


class StockLevelCheckView(View):
    def get(self, request):
        products = db.products.find()
        return render(request, 'stock_level_check.html', {'products': products})
