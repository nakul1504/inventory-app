from bson import Decimal128
from django.db import models

from inventory_management.settings import db


product_collection = db['products']
supplier_collection = db['suppliers']
sale_order_collection = db['sale_orders']
stock_movement_collection = db['stock_movements']



class Supplier:
    def __init__(self, name, email, phone, address):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

    def save(self):
        supplier_data = {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
        }
        return supplier_collection.insert_one(supplier_data)

    @classmethod
    def get_all(cls):
        return list(supplier_collection.find())




class Product:
    def __init__(self, name, description, category, price, stock_quantity, supplier_id):
        self.name = name
        self.description = description
        self.category = category
        self.price = Decimal128(str(price))
        self.stock_quantity = stock_quantity
        self.supplier_id = supplier_id

    def save(self):
        product_data = {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "stock_quantity": self.stock_quantity,
            "supplier_id": self.supplier_id,
        }
        return product_collection.insert_one(product_data)

    @classmethod
    def get_all(cls):
        return list(product_collection.find())

class SaleOrder:
    PENDING = 'Pending'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled')
    ]

    def __init__(self, product_id, product_name ,quantity, total_price, sale_date, status=PENDING):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.total_price = Decimal128(str(total_price))
        self.sale_date = sale_date
        self.status = status

    def save(self):
        sale_order_data = {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "total_price": self.total_price,
            "sale_date": self.sale_date,
            "status": self.status,
        }
        return sale_order_collection.insert_one(sale_order_data)

    @classmethod
    def get_all(cls):
        return list(sale_order_collection.find())

class StockMovement:
    IN = 'In'
    OUT = 'Out'

    MOVEMENT_TYPE_CHOICES = [
        (IN, 'In'),
        (OUT, 'Out')
    ]

    def __init__(self, product_id, quantity, movement_type, movement_date, notes=''):
        self.product_id = product_id
        self.quantity = quantity
        self.movement_type = movement_type
        self.movement_date = movement_date
        self.notes = notes

    def save(self):
        stock_movement_data = {
            "product_id": self.product_id,
            "quantity": self.quantity,
            "movement_type": self.movement_type,
            "movement_date": self.movement_date,
            "notes": self.notes,
        }
        return stock_movement_collection.insert_one(stock_movement_data)

    @classmethod
    def get_all(cls):
        return list(stock_movement_collection.find())