#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from datetime import date
# Create your models here.

class Member(models.Model):
    name = models.CharField("اﻷﺳﻢ ﺑﺎﻟﻜﺎﻣﻞ", max_length = 200)
    job = models.CharField("اﻟﻮﻇﻴﻔﺔ", max_length = 100)
    address = models.CharField("اﻟﻌﻨﻮاﻥ", max_length = 100)
    national_number = models.CharField("اﻟﺮﻗﻢ اﻟﻘﻮﻣﻰ", max_length = 14)
    birth_date = models.DateField("ﺗﺎﺭﻳﺦ اﻟﻤﻴﻼﺩ")
    birth_place = models.CharField("ﺟﻬﺔ اﻟﻤﻴﻼﺩ", max_length = 50, blank = True)
    tel = models.CharField("اﻟﺘﻠﻴﻔﻮﻥ", max_length = 25, blank = True)
    mobile = models.CharField("ﻣﺤﻤﻮﻝ", max_length = 25, blank = True)
    MEMBERSHIP_TYPE = (
        ('M', "ﻣﻨﺘﺴﺐ"),
        ('A', "ﻋﺎﻣﻞ"),
        ('H', "ﻓﺨﺮﻯ"),
    )
    membership_type = models.CharField("ﻧﻮﻉ اﻟﻌﻀﻮﻳﺔ", max_length = 1, choices = MEMBERSHIP_TYPE)
    create_date = models.DateField("ﺗﺤﺮﻳﺮا ﻓﻰ", auto_now_add = True)
    modified_date = models.DateField("ﺗﺎﺭﻳﺦ اﻟﺘﻌﺪﻳﻞ", auto_now = True)
    personal_image = models.ImageField("ﺻﻮﺭﺓ ﺷﺨﺼﻴﺔ", upload_to = '/image', blank = True, null= True)
    membership_id = models.AutoField("ﺭﻗﻢ اﻟﻌﻀﻮﻳﺔ", primary_key = True)

    def __unicode__(self):
        return str(self.membership_id)

    def get_last_paid(self):
        r = self.receipt_set.latest('current_date')
        return r.create_date.year

    
class Receipt(models.Model):
    member = models.ForeignKey(Member)
    rec_number = models.AutoField("ﺭﻗﻢ اﻹﻳﺼﺎﻝ", primary_key = True)
    REC_TYPE = (
        ('Y', "ﺭﺳﻮﻡ ﺃﺷﺘﺮاﻙ ﺳﻨﻮﻳﺔ"),
        ('P', "ﺭﺳﻮﻡ ﺃﺷﺘﺮاﻙ اﻟﻌﻀﻮﻳﺔ"),
    )
    rec_type = models.CharField("ﻧﻮﻉ اﻹﻳﺼﺎﻝ", max_length = 1, choices = REC_TYPE)
    current_date = models.DateField("اﻟﺘﺎﺭﻳﺦ", auto_now_add = True)
    number_of_years = models.IntegerField("ﻋﺪﺩ اﻟﺴﻨﻴﻦ ﻣﺴﺘﺤﻘﺔ اﻟﺪﻓﻊ", default = 1, blank = True, null = True)
    last_paid_year = models.IntegerField("ﻣﻦ", blank = True, null = True)
    #current_year = models.IntegerField("ﺇﻟﻰ", default = date.today().year, blank = True, null = True)

    def __unicode__(self):
        return str(self.rec_number)

    
    

