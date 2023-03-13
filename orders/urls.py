from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('orders/', views.AllOrders.as_view(), name='orders'),
    path('orders-processed/', views.ProcessedOrders.as_view(), name='orders_processed'),
    path('orders-unprocessed/', views.UnprocessedOrders.as_view(), name='orders_unprocessed'),
    path('sausage/', views.Sausage.as_view(), name='sausage'),

    path('customer/', views.CustomerLookup.as_view(), name='customer'),
    path('customer/<pk>/', views.CustomerView.as_view(), name='customer_view'),
    path('customer/<pk>/edit', views.CustomerEdit.as_view(), name='customer_edit'),
    path('customer/<pk>/new_order', views.NewOrder.as_view(), name='new_order'),
    path('customers/', views.AllCustomers.as_view(), name='customers'),
    
    path('order/<pk>/', views.ViewOrder.as_view(), name='view_order'),
    path('order/<pk>/edit', views.EditOrder.as_view(), name='edit_order'),
    path('order/<pk>/process', views.ProcessOrder.as_view(), name='process_order'),
    path('order/<pk>/checkout', views.CheckoutOrder.as_view(), name='checkout_order'),

    path('search/', views.Search.as_view(), name='search'),
    path('export/', views.ExportSausage, name='export'),
]