from django.urls import path
from .views import AddProductView, ProductListView, AddSupplierView, SupplierListView, AddStockMovementView, \
    CreateSaleOrderView, CancelSaleOrderView, CompleteSaleOrderView, SaleOrderListView, StockLevelCheckView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('add-product/', AddProductView.as_view(), name='add-product'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('add-supplier/', AddSupplierView.as_view(), name='add-supplier'),
    path('supplier-list/', SupplierListView.as_view(), name='supplier-list'),
    path('add-stock-movement/', AddStockMovementView.as_view(), name='add-stock-movement'),
    path('create-sale-order/', CreateSaleOrderView.as_view(), name='create-sale-order'),
    path('cancel-sale-order/<str:sale_order_id>/', CancelSaleOrderView.as_view(), name='cancel-sale-order'),
    path('complete-sale-order/<str:sale_order_id>/', CompleteSaleOrderView.as_view(), name='complete-sale-order'),
    path('sale-order-list/', SaleOrderListView.as_view(), name='sale-order-list'),
    path('stock-level-check/', StockLevelCheckView.as_view(), name='stock-level-check'),
]