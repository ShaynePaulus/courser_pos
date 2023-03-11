import csv
from datetime import date, datetime

from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .utils import ordercalc, customerformat
from orders.models import Customer, Order
from orders.forms import CustomerForm, OrderForm, OrderProcess, OrderCheckout

class Index(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.all().order_by('-id')
        contex = {'order_list':orders}
        return render(request, 'orders/index.html', contex)

class CustomerLookup(LoginRequiredMixin, View):
    def get(self, request):
        form = CustomerForm()
        contex = {'form': form}
        return render(request, 'orders/customer_form.html', contex)
    
    def post(self, request):
        form = CustomerForm(request.POST)
        if not form.is_valid():
            contex = {'form': form}
            return render(request, 'orders/customer_form.html', contex)
        #Normalize form data
        customer = form.save(commit=False)
        customerformat(customer)
        #currently assuming customers have unique phone numbers
        try:            
            customer = Customer.objects.get(phone=customer.phone)
            return redirect(reverse('orders:customer_view', args=[customer.id]))
        
        except Customer.DoesNotExist:
            customer.save()
            customer = Customer.objects.get(phone=customer.phone)
            return redirect(reverse_lazy('orders:customer_view', args=[customer.id]))

class CustomerView(LoginRequiredMixin, View):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        previous_orders = list(Order.objects.filter(customer=customer.id).order_by('-id'))
        contex = {'previous_orders': previous_orders, 'customer': customer}
        return render(request, 'orders/customer.html', contex)

class CustomerEdit(LoginRequiredMixin, View):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomerForm(instance=customer)
        contex = {'form': form}
        return render(request, 'orders/customer_form.html', contex)
        
    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomerForm(request.POST, instance=customer)
        if not form.is_valid():
            contex = {'form': form}
            return render(request, 'orders/customer_form.html', contex)
        #Normalize form data
        customer = form.save(commit=False)
        customerformat(customer)
        customer.save()
        return redirect(reverse_lazy('orders:customer_view', args=[customer.id]))

class NewOrder(LoginRequiredMixin, View):
    def get(self, request, pk):
        customer = Customer.objects.get(pk=pk)       
        try:            
            order = Order.objects.filter(customer=customer.id).order_by('-id')[:1]
            order = order[0]
            order.process_paid = False
            order.sausage_paid = False
            form = OrderForm(instance=order)       
        except:
            form = OrderForm()
        contex = {'form': form, 'customer':customer}
        return render(request, 'orders/order_form.html', contex)
    
    def post(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        form = OrderForm(request.POST)
        if not form.is_valid():
            contex = {'form': form, 'customer':customer}
            return render(request, 'orders/order_form.html', contex)
        order = form.save(commit=False)
        order.customer = customer
        ordercalc(order)
        order.save()
        return redirect(reverse_lazy('orders:index'))

class ViewOrder(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        contex = {'order': order}
        return render(request, 'orders/order_view.html', contex)

class EditOrder(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        customer = order.customer
        form = OrderForm(instance=order)
        contex = {'form': form, 'order': order, 'customer': customer}
        return render(request, 'orders/order_form.html', contex)
        
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        customer = order.customer
        form = OrderForm(request.POST, instance=order)
        if not form.is_valid(): 
            contex = {'form': form, 'order': order}
            return render(request, 'orders/order_form.html', contex)
        order.customer = customer
        order = form.save(commit=False)
        ordercalc(order)
        order.save()
        return redirect(reverse_lazy('orders:index'))

class ProcessOrder(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        customer = order.customer
        form = OrderProcess(instance=order)
        contex = {'form': form, 'order': order, 'customer': customer}
        return render(request, 'orders/order_view.html', contex)

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        customer = order.customer
        form = OrderProcess(request.POST)
        if not form.is_valid(): 
            contex = {'form': form, 'order': order}
            return render(request, 'orders/order_form.html', contex)
        form = form.cleaned_data
        order.sausage_out = form['sausage_out']
        order.jerky_out = form['jerky_out']
        order.ham_out = form['ham_out']
        order.bulk_out = form['bulk_out']
        order.freezer = form['freezer']
        order.bag = form['bag']
        order.save()
        return redirect(reverse_lazy('orders:index'))

class CheckoutOrder(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        customer = order.customer
        outform = OrderCheckout(instance=order)
        contex = {'outform': outform, 'order': order, 'customer': customer}
        return render(request, 'orders/order_view.html', contex)

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        customer = order.customer
        outform = OrderCheckout(request.POST)
        if not outform.is_valid():
            contex = {'form': outform, 'order': order}
            return render(request, 'orders/order_form.html', contex)
        outform = outform.cleaned_data
        #'process_paid', 'sausage_paid', 'payment_style', 'order_gone', 'sausage_gone'
        order.process_paid = outform['process_paid']
        order.sausage_paid = outform['sausage_paid']
        order.payment_style = outform['payment_style']
        order.order_gone = outform['order_gone']
        order.sausage_gone = outform['sausage_gone']
        if order.order_gone:
            order.checkout_date = datetime.now()
        if order.sausage_gone:
            order.sausage_date = datetime.now()
        order.save()
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
            return redirect(reverse_lazy('orders:customer_view', args=[customer.id]))
        except:
            pass
        
        return HttpResponse(f'No entries matching "{search}"')

class Sausage(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse('Working on this')

def ExportCsv(request):
    response = HttpResponse()
    today = date.today()
    response['Content-Disposition'] = (f'attachment; filename={today}-orders.csv')
    writer = csv.writer(response)
    writer.writerow(['Order ID', 'First', 'Last',
                        'Customer ID', 'Payment_style'])
    order_fields = Order.objects.all().values_list('id', 'customer', 'payment_style')
    for order in order_fields:
        first = getattr(Customer.objects.get(pk=order[1]), 'first')
        last = getattr(Customer.objects.get(pk=order[1]), 'last')
        order = list(order)
        order.insert(1, first)
        order.insert(2, last)
        writer.writerow(order)
    return response
