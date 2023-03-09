from django import forms
from django.forms import ModelForm
from .models import Customer, Order
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, HTML, Layout, Row, Div, Fieldset, ButtonHolder, Column
from django.urls import reverse

class CustomerForm(ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-primary',
                             onclick="window.location.href = '{}';".format(reverse('orders:index'))))

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()