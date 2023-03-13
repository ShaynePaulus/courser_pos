from django.db import models

# Create your models here.
class Customer(models.Model):
    first = models.CharField(max_length=50)
    last = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return (self.first + ' ' + self.last)

class Order(models.Model):    
    PAYMENT_CHOICES = [('None', 'Not Paid'), ('Cash', 'Cash'), ('Credit', 'Credit'), ('Check', 'Check'), ('Free', 'Free')]
    GENDER_CHOICES = [('Doe', 'Doe'), ('Buck', 'Buck')]
    POINT_CHOICES = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13),  (14, 14), (15, 15),  (16, 16),]
    MOUNT_CHOICES = [('Antlers', 'Antler Mount'), ('Euro', 'Euro Mount'), ('Shoulder', 'Shoulder Mount')]
    HIDE_CHOICES = [('Yes', 'Keep Hide ($10)')]
    STEAK_CHOICES = [('Steaks', 'Steaks'), ('Whole', 'Whole'), ('Burger', 'Burger')]
    TENDER_CHOICES = [('Steaks', 'Steaks'), ('Whole', 'Whole'), ('Burger', 'Burger'), ('Removed', 'Removed')]
    BURGER_CHOICES = [('Ground', 'Ground Burger'), ('Sausage', 'All Sausage')]
    ROAST_CHOICES = [('', 'None'), ('1', 'One'), ('2', 'Two'), ('3', 'Three'), ('All', 'All')]
    PACKAGE_CHOICES = [('1/2 lb', '1/2 lb'), ('1 lb', '1 lb'), ('1 1/2 lb', '1 1/2 lb'), ('2 lb', '2 lb'), ('2 1/2lb', '2 1/2lb'), ('3 lb', '3 lb'), ]
    SAUSAGE_CHOICES = [('1', 'One'), ('2', 'Two'), ('3', 'Three'), ('4', 'Four'), ('5', 'Five'), ('All', 'All')]
    BULK_CHOICES = [('3', '3 lbs'), ('6', '6 lbs'), ('9', '9 lbs'), ('All', 'All')]
    
    #process info
    sausage_out = models.BooleanField(default= False, blank=True, null=True)
    bulk_out = models.BooleanField(default= False, blank=True, null=True)
    ham_out = models.BooleanField(default= False, blank=True, null=True)
    jerky_out = models.BooleanField(default= False, blank=True, null=True)

    freezer = models.IntegerField(null=True)
    bag = models.IntegerField(null=True)

    contact_date = models.DateTimeField(blank=True, null=True)
    sausage_ordered = models.BooleanField(blank=True, null=True)

    #checkout info
    #can delete order_gone
    order_gone = models.BooleanField(default=False, blank=True, null=True)
    sausage_gone = models.BooleanField(default=False, blank=True, null=True)
    process_paid = models.BooleanField(default=False, null=True)
    sausage_paid = models.BooleanField(default=False, null=True)

    checkout_date = models.DateTimeField(blank=True, null=True)
    sausage_date = models.DateTimeField(blank=True, null=True)
    payment_style = models.CharField(max_length=6, choices=PAYMENT_CHOICES, blank=True)

    
    #cost info
    hide_cost= models.IntegerField(default = 0, blank=True)
    sausage_cost = models.FloatField(default = 0, blank=True)
    smoked_cost = models.FloatField(default = 0, blank=True)
    bulk_cost = models.FloatField(default = 0, blank=True)
    process_cost = models.IntegerField(blank=True)
    total_cost = models.FloatField(blank=True)

    #auto filled
    process_date = models.DateTimeField(blank=True, null=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, blank=True)
    checkin_date = models.DateField(auto_now_add=True)
    checkin_time = models.TimeField(auto_now_add=True)

    #deer info
    tag_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=4, choices=GENDER_CHOICES, default='doe')
    points = models.IntegerField(choices=POINT_CHOICES, blank=True, null=True)
    mount = models.CharField(max_length=8, choices=MOUNT_CHOICES, blank=True, null=True)
    hide = models.CharField(max_length=4, choices=HIDE_CHOICES, blank=True, null=True)

    #cut options
    loins = models.CharField(max_length=6,choices=STEAK_CHOICES, default='Steaks')
    tender_loins = models.CharField(max_length=7,choices=TENDER_CHOICES, default='Steaks')
    rounds = models.CharField(max_length=6,choices=STEAK_CHOICES, default='Steaks')
    tips = models.CharField(max_length=6,choices=STEAK_CHOICES, default='Steaks')
    burger = models.CharField(max_length=11,choices=BURGER_CHOICES, default='Ground')
    shoulder_roast = models.CharField(max_length=3,choices=ROAST_CHOICES, blank=True, null=True)
    neck_roast = models.CharField(max_length=3,choices=ROAST_CHOICES, blank=True, null=True)
    
    #package options
    package_size = models.CharField(max_length=8,choices=PACKAGE_CHOICES, default='1 lb')
    notes = models.TextField(blank=True, null=True)

    #sausage options
    smoked_lbs = models.IntegerField(blank=True, null=True)
    original_summer_sausage = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)
    cheese_summer_sausage = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)
    jalapeno_summer_sausage = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)
    hickory_stick = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)
    original_pepper_sticks = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)
    jalapeno_pepper_sticks = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)
    hunter_twiggs = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)
    honey_bbq_pepper_sticks = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)
    smoked_brats = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)
    jalapeno_smoked_brats = models.CharField(max_length=3,choices=SAUSAGE_CHOICES, blank=True, null=True)

    #ham/jerky options
    jerky_lbs = models.IntegerField(blank=True, null=True)
    smoked_ham = models.IntegerField(choices=[(1, 'One'), (2, 'Two')], blank=True, null=True)
    jerky = models.CharField(max_length=3, choices=SAUSAGE_CHOICES, blank=True, null=True)
    jerky_sweet_and_spicy = models.CharField(max_length=3, choices=SAUSAGE_CHOICES, blank=True, null=True)

    #bulk options
    bulk_lbs = models.FloatField(blank=True, null=True)
    maple_breakfast = models.CharField(max_length=3, choices=BULK_CHOICES, blank=True, null=True)
    spicy_breakfast = models.CharField(max_length=3, choices=BULK_CHOICES, blank=True, null=True)
    italian = models.CharField(max_length=3, choices=BULK_CHOICES, blank=True, null=True)

    def __str__(self):
        return str(self.id)