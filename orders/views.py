import csv
from datetime import date, datetime
import phonenumbers

from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db.models import Q

from .utils import ordercalc, customerformat
from orders.models import Customer, Order
from orders.forms import CustomerForm, OrderForm, OrderProcess, OrderCheckout

class Index(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.all().order_by('-id')[:20]
        context = {'order_list':orders,}
        return render(request, 'orders/index.html', context)

class AllOrders(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.all().order_by('-id')
        context = {'order_list':orders, 'key': 'All'}
        return render(request, 'orders/index.html', context)

class ProcessedOrders(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(checkout_date= None).exclude(process_date= None).order_by('-id')
        context = {'order_list':orders, 'key': 'Checkout'}
        return render(request, 'orders/index.html', context)

class UnprocessedOrders(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(process_date= None).order_by('-id')
        context= {'order_list':orders, 'key': 'Unprocessed'}
        return render(request, 'orders/index.html', context)

class Sausage(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(sausage_date= None).exclude(process_date= None).order_by('-id')
        context = {'order_list':orders, 'key': 'Sausage','sausagebutton':'1'}
        return render(request, 'orders/index.html', context)

class AllCustomers(LoginRequiredMixin, View):
    def get(self, request):
        customers = Customer.objects.all().order_by('-id')
        context = {'customer_list':customers, 'key': 'All'}
        return render(request, 'orders/customer_index.html', context)

class CustomerLookup(LoginRequiredMixin, View):
    def get(self, request):
        form = CustomerForm()
        context = {'form': form}
        return render(request, 'orders/customer_form.html', context)
    
    def post(self, request):
        form = CustomerForm(request.POST)
        if not form.is_valid():
            context = {'form': form}
            return render(request, 'orders/customer_form.html', context)
        #Normalize form data
        customer = form.save(commit=False)
        customerformat(customer)
        #currently assuming customers have unique phone numbers and first names
        try:            
            existing_customer = Customer.objects.filter(phone=customer.phone).filter(first=customer.first)
            existing_customer = existing_customer[0]
            return redirect(reverse('orders:customer_view', args=[existing_customer.id]))       
        except:
            customer.save()
            customer = Customer.objects.filter(phone=customer.phone).filter(first=customer.first)
            customer = customer[0]
            return redirect(reverse_lazy('orders:customer_view', args=[customer.id]))

class CustomerView(LoginRequiredMixin, View):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        previous_orders = list(Order.objects.filter(customer=customer.id).order_by('-id'))
        context = {'previous_orders': previous_orders, 'customer': customer}
        return render(request, 'orders/customer.html', context)

class CustomerEdit(LoginRequiredMixin, View):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomerForm(instance=customer)
        context = {'form': form}
        return render(request, 'orders/customer_form.html', context)
        
    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomerForm(request.POST, instance=customer)
        if not form.is_valid():
            context = {'form': form}
            return render(request, 'orders/customer_form.html', context)
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
        context = {'form': form, 'customer':customer}
        return render(request, 'orders/order_form.html', context)
    
    def post(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        form = OrderForm(request.POST)
        if not form.is_valid():
            context = {'form': form, 'customer':customer}
            return render(request, 'orders/order_form.html', context)
        order = form.save(commit=False)
        order.customer = customer
        ordercalc(order)
        order.save()
        return redirect(reverse_lazy('orders:view_order', args=[order.id]))

class ViewOrder(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        context = {'order': order}
        return render(request, 'orders/order_view.html', context)

class EditOrder(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        customer = order.customer
        form = OrderForm(instance=order)
        context = {'form': form, 'order': order, 'customer': customer}
        return render(request, 'orders/order_form.html', context)
        
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        customer = order.customer
        form = OrderForm(request.POST, instance=order)
        if not form.is_valid(): 
            context = {'form': form, 'order': order}
            return render(request, 'orders/order_form.html', context)
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
        context = {'form': form, 'order': order, 'customer': customer}
        return render(request, 'orders/order_view.html', context)

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        customer = order.customer
        form = OrderProcess(request.POST)
        if not form.is_valid(): 
            context = {'form': form, 'order': order}
            return render(request, 'orders/order_form.html', context)
        form = form.cleaned_data
        order.sausage_out = form['sausage_out']
        order.jerky_out = form['jerky_out']
        order.ham_out = form['ham_out']
        order.bulk_out = form['bulk_out']
        order.freezer = form['freezer']
        order.bag = form['bag']
        if order.bag != None:
            order.process_date = datetime.now()
        order.save()
        return redirect(reverse_lazy('orders:index'))

class CheckoutOrder(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        customer = order.customer
        outform = OrderCheckout(instance=order)
        context = {'outform': outform, 'order': order, 'customer': customer}
        return render(request, 'orders/order_view.html', context)

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        customer = order.customer
        outform = OrderCheckout(request.POST)
        if not outform.is_valid():
            context = {'form': outform, 'order': order}
            return render(request, 'orders/order_form.html', context)
        outform = outform.cleaned_data
        #'process_paid', 'sausage_paid', 'payment_style', 'order_gone', 'sausage_gone'
        order.process_paid = outform['process_paid']
        order.sausage_paid = outform['sausage_paid']
        order.payment_style = outform['payment_style']
        order.order_gone = outform['order_gone']
        order.sausage_gone = outform['sausage_gone']
        if order.order_gone:
            order.checkout_date = datetime.now()
        else:
            order.checkout_date = None
        if order.sausage_gone:
            order.sausage_date = datetime.now()
        else:
            order.sausage_date = None
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
            searchphone = phonenumbers.format_number(phonenumbers.parse(search, 'US'), phonenumbers.PhoneNumberFormat.E164)
            customers = Customer.objects.filter(phone=searchphone).order_by('id')
            context = {'customer_list':customers, 'key': 'All'}
            return render(request, 'orders/customer_index.html', context)
        except:
            pass
        #search for customer by first and last. 
        try:
            searchname = search.title()
            customers = Customer.objects.filter(Q(first=searchname) | Q(last=searchname)).order_by('id')
            print(customers)
            context = {'customer_list':customers, 'key': 'All'}
            return render(request, 'orders/customer_index.html', context)
        except:
            pass     
        return HttpResponse(f'No entries matching "{search}"')

def ExportSausage(request):
    response = HttpResponse()
    today = date.today()
    response['Content-Disposition'] = (f'attachment; filename={today}-sausage-orders.csv')
    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Customer', 
                        'Smoked Lbs', 'original_summer_sausage', 'cheese_summer_sausage', 'jalapeno_summer_sausage', 'hickory_stick', 
                                'original_pepper_sticks', 'jalapeno_pepper_sticks','hunter_twiggs','honey_bbq_pepper_sticks', 'smoked_brats', 'jalapeno_smoked_brats',
                        'Jerky Lbs', 'jerky', 'jerky_sweet_and_spicy',
                        'Smoked Ham'])
    writer.writerow(['Total', '', '=SUM(C3:C999)', '=SUM(D3:D999)', '=SUM(E3:E999)', '=SUM(F3:F999)', '=SUM(G3:G999)', '=SUM(H3:H999)', '=SUM(I3:I999)', '=SUM(J3:J999)',
                        '=SUM(K3:K999)', '=SUM(L3:L999)', '=SUM(M3:M999)', '=SUM(N3:N999)', '=SUM(O3:O999)', '=SUM(P3:P999)', '=SUM(Q3:Q999)'])
    sausage_orders = Order.objects.filter(~Q(smoked_lbs=0)|~Q(jerky_lbs=0)|~Q(smoked_ham=0)).exclude(sausage_ordered=True)\
        .values_list('id', 'customer',
                        'smoked_lbs', 'original_summer_sausage', 'cheese_summer_sausage', 'jalapeno_summer_sausage', 'hickory_stick', 
                            'original_pepper_sticks', 'jalapeno_pepper_sticks','hunter_twiggs','honey_bbq_pepper_sticks', 'smoked_brats', 'jalapeno_smoked_brats',
                        'jerky_lbs', 'jerky', 'jerky_sweet_and_spicy',
                        'smoked_ham')
    for order in sausage_orders:
        ordered = Order.objects.get(id=order[0])
        ordered.sausage_ordered = True
        ordered.save()
        order = list(order)
        customer = list(Customer.objects.filter(pk=order[1]))
        order[1] = customer[0]
        writer.writerow(order)
    
    return response
