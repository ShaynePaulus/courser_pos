import phonenumbers

def ordercalc(order):
    #Processing Cost
    PROCESSING_COST = 75
    HIDE_COST = 10

    #Sausage Costs
    original_summer_sausage = 17
    cheese_summer_sausage = 20
    jalapeno_summer_sausage = 20
    hickory_stick = 17
    original_pepper_sticks = 28
    jalapeno_pepper_sticks = 32
    hunter_twiggs = 28
    honey_bbq_pepper_sticks = 28
    smoked_brats = 24
    jalapeno_smoked_brats = 28

    smoked_ham = 17
    jerky = 8
    jerky_sweet_and_spicy = 8

    maple_breakfast = 2.5
    spicy_breakfast = 2.5
    italian = 2.5

    #Weights
    SSLB = 3
    PSLB = 4
    SBLB = 4

    #calculate lbs
    order.smoked_ham = int(order.smoked_ham or 0)
    order.smoked_lbs = ((SSLB *
                            (int(order.original_summer_sausage or 0)+
                            int(order.cheese_summer_sausage or 0)+
                            int(order.jalapeno_summer_sausage or 0)+
                            int(order.hickory_stick or 0))
                        )
                        +(PSLB * 
                            (int(order.original_pepper_sticks or 0)+
                            int(order.jalapeno_pepper_sticks or 0)+
                            int(order.hunter_twiggs or 0)+
                            int(order.honey_bbq_pepper_sticks or 0))
                        )
                        +(SBLB *
                            (int(order.smoked_brats or 0)+
                            int(order.jalapeno_smoked_brats or 0))
                        ))
    order.jerky_lbs = (int(order.jerky or 0)+
                        int(order.jerky_sweet_and_spicy or 0))
    order.bulk_lbs = (int(order.maple_breakfast or 0)+
                        int(order.spicy_breakfast or 0)+
                        int(order.italian or 0))

    #calculate costs
    if order.hide or order.mount == 'Shoulder':
        order.hide_cost = HIDE_COST
    
    order.process_cost = PROCESSING_COST
    if order.payment_style == 'Free':
        order.process_cost = 0.0
        order.process_paid = True
        
    order.smoked_cost = (                       
                        (int(order.original_summer_sausage or 0)* original_summer_sausage)+
                        (int(order.cheese_summer_sausage or 0)* cheese_summer_sausage)+
                        (int(order.jalapeno_summer_sausage or 0)* jalapeno_summer_sausage)+
                        (int(order.hickory_stick or 0)* hickory_stick)+
                        (int(order.original_pepper_sticks or 0)* original_pepper_sticks)+
                        (int(order.jalapeno_pepper_sticks or 0)* jalapeno_pepper_sticks)+
                        (int(order.hunter_twiggs or 0)* hunter_twiggs)+
                        (int(order.honey_bbq_pepper_sticks or 0)* honey_bbq_pepper_sticks)+
                        (int(order.smoked_brats or 0)* smoked_brats)+
                        (int(order.jalapeno_smoked_brats or 0)* jalapeno_smoked_brats)+
                        (int(order.smoked_ham or 0)* smoked_ham)+
                        (int(order.jerky or 0)* jerky)+
                        (int(order.jerky_sweet_and_spicy or 0)* jerky_sweet_and_spicy)
                        )

    order.bulk_cost = ((int(order.maple_breakfast or 0) * maple_breakfast) + 
                        (int(order.spicy_breakfast or 0) * spicy_breakfast) + 
                        (int(order.italian or 0) * italian))

    order.sausage_cost = (order.bulk_cost + order.smoked_cost)

    order.total_cost = (order.process_cost + order.sausage_cost + int(order.hide_cost or 0))

    order.tag_number = order.tag_number.upper()

def customerformat(customer):
    customer.phone = phonenumbers.format_number(phonenumbers.parse(customer.phone, 'US'), phonenumbers.PhoneNumberFormat.E164)
    customer.first = customer.first.title()
    customer.last = customer.last.title()