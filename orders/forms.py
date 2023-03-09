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
        exclude = ('customer',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Fieldset(
                'Deer Info',
                'tag_number',
                Div(
                    Div('Gender', css_class='col-sm'),
                    Div('Points', css_class='col-sm'),
                    Div('Mount', css_class='col-sm'),
                    Div('Hide', css_class='col-sm'),
                css_class='form-row'),
            ),
            Fieldset(
                'Cut Options',
                HTML('''<p>Steaks<p>'''),
                Div(
                    Div('Loins', css_class='col-sm'),
                    Div('Tender_Loins', css_class='col-sm'),
                css_class='form-row'),
                Div(
                    Div('Rounds', css_class='col-sm'),
                    Div('Tips', css_class='col-sm'),
                css_class='form-row'),
                HTML('''<p>Roasts & Burger<p>'''),
                Div(
                    Div('Shoulder_roast', css_class='col-sm'),
                    Div('Neck_Roast', css_class='col-sm'),
                css_class='form-row'),
                Div(
                    Div('Burger', css_class='col-sm'),
                    Div(css_class='col-sm'),
                css_class='form-row'),
            ),
            Fieldset(
                'Sausage Options',
                HTML('''<p>Summer Sausages<p>'''),
                Div(
                    Div('Original_Summer_Sausage', css_class='col-sm'),
                    Div('Cheese_Summer_Sausage', css_class='col-sm'),
                    Div('Jalap_Summer_Sausage', css_class='col-sm'),
                    Div('Hickory_Stick', css_class='col-sm'),
                css_class='form-row'),
                HTML('''<p>Pepper Sticks<p>'''),
                Div(
                    Div('Original_Pepper_Sticks', css_class='col-sm'),
                    Div('Jalapeno_Cheese_Pepper_Sticks', css_class='col-sm'),
                    Div('Hunter_Twiggs', css_class='col-sm'),
                    Div('Honey_BBQ_Pepper_Sticks', css_class='col-sm'),
                css_class='form-row'),
                HTML('''<p>Brats<p>'''),
                Div(
                    Div('Smoked_Brats', css_class='col-sm'),
                    Div('Jalapeno_Smoked_Brats', css_class='col-sm'),
                    Div(css_class='col-sm'),
                    Div(css_class='col-sm'),
                css_class='form-row'),
                HTML('''<p>Ham & Jerky<p>'''),
                Div(
                    Div('smoked_ham', css_class='col-sm'),
                    Div('jerky', css_class='col-sm'),
                    Div('jerky_sweet_and_spicy', css_class='col-sm'),
                    Div(css_class='col-sm'),
                css_class='form-row'),
            ),
            Fieldset(
                'House Sausage Options',
                Div(
                    Div('maple_breakfast', css_class='col-sm'),
                    Div('spicy_breakfast', css_class='col-sm'),
                css_class='form-row'),
                Div(
                    Div('italian', css_class='col-sm'),
                    Div(css_class='col-sm'),
                css_class='form-row'),                
            ),
            Fieldset(
                'Package, Notes & Payment',
                Div(
                    Div('Package_Size', css_class='col-sm'),
                css_class='form-row'),
                Div(
                    Div('Notes', css_class='col-sm'),
                css_class='form-row'),
                Div(
                    Div('process_paid', css_class='col-sm'),
                    Div('sausage_paid', css_class='col-sm'),
                    Div('payment_style', css_class='col-sm'),
                css_class='form-row'),
            ),
        )
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-primary',
                             onclick="window.history.go(-1); return false;"))