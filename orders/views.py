from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


import phonenumbers

from .models import Customer, Order
from orders.forms import CustomerForm, OrderForm

class Index(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.all().order_by('-id')
        contex = {'order_list':orders}
        return render(request, 'orders/index.html', contex)

class CustomerSearch(LoginRequiredMixin, View):
    def get(self, request):
        form = CustomerForm()
        ctx = {'form': form}
        return render(request, 'orders/customer_form.html', ctx)
    
    def post(self, request):
        form = CustomerForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, 'orders/customer_form.html', ctx)
        #Normalize form data
        customer = form.save(commit=False)
        customer.phone = phonenumbers.format_number(phonenumbers.parse(customer.phone, 'US'), phonenumbers.PhoneNumberFormat.E164)
        customer.first = customer.first.title()
        customer.last = customer.last.title()
        #currently assuming customers have unique phone numbers
        try:            
            customer = Customer.objects.get(phone=customer.phone)
            print('customer not found')
            return redirect(reverse('orders:customer_view', args=[customer.id]))
        
        except Customer.DoesNotExist:
            customer.save()
            customer = Customer.objects.get(phone=customer.phone)
            return redirect(reverse_lazy('orders:customer_view', args=[customer.id]))

class CustomerView(LoginRequiredMixin, View):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        previous_orders = list(Order.objects.filter(customer=customer.id))
        ctx = {'previous_orders': previous_orders, 'customer': customer}
        return render(request, 'orders/customer.html', ctx)

class CustomerEdit(LoginRequiredMixin, View):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomerForm(instance=customer)
        ctx = {'form': form}
        return render(request, 'orders/customer_form.html', ctx)
        
    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomerForm(request.POST, instance=customer)
        if not form.is_valid():
            errors = form.errors
            print(errors)
            ctx = {'form': form, 'error': errors}
            return render(request, 'orders/customer_form.html', ctx)
        #Normalize form data
        customer = form.save(commit=False)
        customer.phone = phonenumbers.format_number(phonenumbers.parse(customer.phone, 'US'), phonenumbers.PhoneNumberFormat.E164)
        customer.first = customer.first.title()
        customer.last = customer.last.title()
        customer.save()
        return redirect(reverse_lazy('orders:customer_view', args=[customer.id]))

class NewOrder(LoginRequiredMixin, View):
    def get(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        form = OrderForm()
        ctx = {'form': form, 'customer':customer}
        return render(request, 'orders/order_form.html', ctx)
    
    def post(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        form = OrderForm(request.POST)
        if not form.is_valid():
            errors = form.errors
            ctx = {'form': form, 'error': errors, 'customer':customer}
            return render(request, 'orders/order_form.html', ctx)
        order = form.save(commit=False)
        order.customer = customer
        order.save()
        return redirect(reverse_lazy('orders:index'))

class ViewOrder(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        contex = {'order': order}
        return render(request, 'orders/view_order.html', contex)

class EditOrder(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        form = OrderForm(instance=order)
        contex = {'form': form}
        return render(request, 'orders/order_form.html', contex)
        
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        form = OrderForm(request.POST, instance=order)
        if not form.is_valid():
            errors = form.errors
            ctx = {'form': form, 'error': errors}
            return render(request, 'orders/order_form.html', ctx)
        form.save()
        return redirect(reverse_lazy('orders:index'))

class Search(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse('TODO: MAKE SEARCH HTML')

    def post(self, request):
        search = request.POST['search']
        #search for order by order number
        try:
            order = Order.objects.get(pk=search)
            pk = order.id
            return redirect(reverse_lazy('orders:view_order', args=[pk]))
        except:
            pass
        #search for customer by tag_number and phone.        
        try:
            orders = list(Order.objects.filter(tag_number=search))
            return redirect(reverse_lazy('orders:customer_view', args=[orders[0].customer.id]))
        except:
            pass
        try:
            search = phonenumbers.format_number(phonenumbers.parse(search, 'US'), phonenumbers.PhoneNumberFormat.E164)
            customer = Customer.objects.get(phone=search)
            return HttpResponse('found customer by phone')
        except:
            pass
        #search for customer by first and last. 
        search = search.title()
        try:            
            customer = Customer.objects.get(first=search)
            return redirect(reverse_lazy('orders:customer_view', args=[customer.id]))
        except:
            pass
        try:
            customer = Customer.objects.get(last=search)
            return HttpResponse('found customer by last')
        except:
            pass
        
        return HttpResponse(f'No entries matching "{search}"')

