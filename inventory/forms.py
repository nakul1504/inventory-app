import re

from bson import ObjectId
from django import forms
from django.core.exceptions import ValidationError

from inventory_management.settings import db

class ProductForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=True
    )
    category = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.00,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    stock_quantity = forms.IntegerField(
        min_value=0,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    supplier = forms.ChoiceField(
        choices=[],
        required=True,
        label="Supplier",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

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
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter supplier name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter supplier email'})
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'})
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter supplier address'}),
        required=True
    )


    def clean_phone(self):
            phone = self.cleaned_data.get('phone')
            if not re.match(r'^\d{10}$', phone):
                raise ValidationError("Phone number must be exactly 10 digits.")
            return phone


class StockMovementForm(forms.Form):
    product = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'})
    )
    movement_type = forms.ChoiceField(
        choices=[('In', 'Incoming'), ('Out', 'Outgoing')],
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter any notes'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        product_choices = [(str(product['_id']), product['name']) for product in db.products.find()]
        self.fields['product'].choices = product_choices

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise ValidationError("Quantity must be a positive number.")
        return quantity

class SaleOrderForm(forms.Form):
    product = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'})
    )

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