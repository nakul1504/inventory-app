import re

from bson import ObjectId
from django import forms
from django.core.exceptions import ValidationError

from inventory_management.settings import db

class ProductForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    category = forms.CharField(max_length=255, required=True)
    price = forms.DecimalField(max_digits=10, decimal_places=2,min_value=0.00, required=True)
    stock_quantity = forms.IntegerField(min_value=0, required=True)
    supplier_choices = [(str(supplier['_id']), supplier['name']) for supplier in db.suppliers.find()]
    supplier = forms.ChoiceField(choices=[], required=True, label="Supplier")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        supplier_choices = [(str(supplier['_id']), supplier['name']) for supplier in db.suppliers.find()]
        self.fields['supplier'].choices = supplier_choices

    def clean_stock_quantity(self):
        stock_quantity = self.cleaned_data.get('stock_quantity')
        if stock_quantity < 0:
            raise ValidationError("Stock quantity cannot be negative.")
        return stock_quantity

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price


class SupplierForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\d{10}$', phone):
            raise ValidationError("Phone number must be exactly 10 digits.")
        return phone


class StockMovementForm(forms.Form):
    product = forms.ChoiceField(required=True)
    quantity = forms.IntegerField(min_value=1, required=True)
    movement_type = forms.ChoiceField(choices=[('In', 'Incoming'), ('Out', 'Outgoing')], required=True)
    notes = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(StockMovementForm, self).__init__(*args, **kwargs)
        product_choices = [(str(product['_id']), product['name']) for product in db.products.find()]
        self.fields['product'].choices = product_choices

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise ValidationError("Quantity must be a positive number.")
        return quantity

class SaleOrderForm(forms.Form):
    product = forms.ChoiceField(required=True)
    quantity = forms.IntegerField(min_value=1, required=True)

    def __init__(self, *args, **kwargs):
        super(SaleOrderForm, self).__init__(*args, **kwargs)
        product_choices = [(str(product['_id']), product['name']) for product in db.products.find()]
        self.fields['product'].choices = product_choices

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product_id = self.cleaned_data.get('product')

        product = db.products.find_one({"_id": ObjectId(product_id)})
        if product and quantity > product['stock_quantity']:
            raise ValidationError(f"Not enough stock available. Only {product['stock_quantity']} items in stock.")
        return quantity