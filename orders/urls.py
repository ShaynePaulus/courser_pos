from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('customer/', views.CustomerSearch.as_view(), name='customer_search'),
    path('customer/<pk>/', views.CustomerView.as_view(), name='customer_view'),
    path('customer/<pk>/edit', views.CustomerEdit.as_view(), name='customer_edit'),
    path('customer/<pk>/new_order', views.NewOrder.as_view(), name='new_order'),
    path('order/<pk>/', views.ViewOrder.as_view(), name='view_order'),
    path('order/<pk>/edit', views.EditOrder.as_view(), name='edit_order'),
    path('search/', views.Search.as_view(), name='search'),
]