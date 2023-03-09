from django.db import models
from django.core.validators import MinLengthValidator

PROCESSING_COST = 75    
PAYMENT_CHOICES = [('none', 'Not Paid'), ('cash', 'Cash'), ('credit', 'Credit'), ('check', 'Check'), ('free', 'Free')]
GENDER_CHOICES = [('Doe', 'Doe'), ('Buck', 'Buck')]
POINT_CHOICES = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13),  (14, 14), (15, 15),  (16, 16),]
MOUNT_CHOICES = [('Antlers', 'Antler Mount'), ('Euro', 'Euro Mount'), ('Shoulder', 'Shoulder Mount')]
HIDE_CHOICES = [('Yes', 'Keep Hide ($10)')]
STEAK_CHOICES = [('Steaks', 'Steaks'), ('Whole', 'Whole'), ('Burger', 'Burger')]
BURGER_CHOICES = [('Ground', 'Ground Burger'), ('All Sausage', 'All Sausage')]
ROAST_CHOICES = [('0', 'None'), ('1', 'One'), ('2', 'Two'), ('3', 'Three'), ('4', 'Four'), ('All', 'All')]
PACKAGE_CHOICES = [(.5, '1/2 lb'), (1, '1 lb'), (1.5, '1 1/2 lb'), (2, '2 lb'), (2.5, '2 1/2lb'), (3, '3 lb'), ]
SAUSAGE_CHOICES = [('0', 'None'), ('1', 'One'), ('2', 'Two'), ('3', 'Three'), ('4', 'Four'), ('5', 'Five'), ('All', 'All')]
BULK_CHOICES = [('3', '3 lbs'), ('6', '6 lbs'), ('9', '9 lbs'), ('All', 'All')]
# Create your models here.
class Customer(models.Model):
    first = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(2, "First name must be greater than 1 character")]
    )
    last = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(2, "First name must be greater than 1 character")]
    )
    phone = models.CharField(max_length=15)

    def __str__(self):
        return (self.first + ' ' + self.last)

class Order(models.Model):
    #auto filled
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    checkin_date = models.DateField(auto_now_add=True)
    checkin_time = models.TimeField(auto_now_add=True)

    #order info to update later
    process_date = models.DateField(blank=True, null=True)
    sausage_taken = models.BooleanField(blank=True, null=True)
    sausage_ordered = models.BooleanField(blank=True, null=True)
    contact_date = models.DateTimeField(blank=True, null=True)
    
    #cost info
    processing_cost = models.IntegerField(default = PROCESSING_COST, blank=True)
    sausage_cost = models.FloatField(default = 0, blank=True)
    bulk_cost = models.FloatField(default = 0, blank=True)
    total_cost = models.FloatField(blank=True, null=True)

    #deer info
    tag_number = models.CharField(max_length=20)
    Gender = models.CharField(max_length=4, choices=GENDER_CHOICES, default='doe')
    Points = models.IntegerField(default = 0, choices=POINT_CHOICES, blank=True)
    Mount = models.CharField(max_length=8, choices=MOUNT_CHOICES, blank=True)
    Hide = models.CharField(max_length=4, choices=HIDE_CHOICES, blank=True)

    #cut options
    Loins = models.CharField(max_length=6,choices=STEAK_CHOICES, default='Steaks')
    Tender_Loins = models.CharField(max_length=6,choices=STEAK_CHOICES, default='Steaks')
    Rounds = models.CharField(max_length=6,choices=STEAK_CHOICES, default='Steaks')
    Tips = models.CharField(max_length=6,choices=STEAK_CHOICES, default='Steaks')
    Burger = models.CharField(max_length=11,choices=BURGER_CHOICES, default='Ground')
    Shoulder_roast = models.CharField(max_length=3,choices=ROAST_CHOICES, default='0')
    Neck_Roast = models.CharField(max_length=3,choices=ROAST_CHOICES, default='0')
    
    #package options
    Package_Size = models.FloatField(max_length=3,choices=PACKAGE_CHOICES, default=1)
    Notes = models.TextField(blank=True)

    #sausage options
    Original_Summer_Sausage = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)
    Cheese_Summer_Sausage = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)
    Jalap_Summer_Sausage = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)
    Hickory_Stick = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)
    Original_Pepper_Sticks = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)
    Jalapeno_Cheese_Pepper_Sticks = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)
    Hunter_Twiggs = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)
    Honey_BBQ_Pepper_Sticks = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)
    Smoked_Brats = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)
    Jalapeno_Smoked_Brats = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)

    #ham/jerky options
    smoked_ham = models.IntegerField(choices=[(1, 'One'), (2, 'Two')], blank=True, null=True)
    jerky = models.CharField(max_length=3, choices=SAUSAGE_CHOICES, blank=True, null=True)
    jerky_sweet_and_spicy = models.CharField(max_length=3, choices=SAUSAGE_CHOICES, blank=True, null=True)

    #bulk options
    maple_breakfast = models.CharField(max_length=3, choices=BULK_CHOICES, blank=True, null=True)
    spicy_breakfast = models.CharField(max_length=3, choices=BULK_CHOICES, blank=True, null=True)
    italian = models.CharField(max_length=3, choices=BULK_CHOICES, blank=True, null=True)

    #payment
    payment_style = models.CharField(max_length=6, choices=PAYMENT_CHOICES, default='none', blank=True)
    process_paid = models.BooleanField(default=False)
    sausage_paid = models.BooleanField(default=False)

    
    