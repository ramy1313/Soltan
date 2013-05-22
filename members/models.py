#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from datetime import date
# Create your models here.

class Member(models.Model):
    name = models.CharField("الأسم بالكامل", max_length = 200)
    job = models.CharField("الوظيفة", max_length = 100)
    address = models.CharField("العنوان", max_length = 100)
    national_number = models.CharField("الرقم القومى", max_length = 14)
    birth_date = models.DateField("تاريخ الميلاد")
    birth_place = models.CharField("جهة الميلاد", max_length = 50, blank = True)
    tel = models.CharField("التليفون", max_length = 25, blank = True)
    mobile = models.CharField("محمول", max_length = 25, blank = True)
    MEMBERSHIP_TYPE = (
        ('M', "منتسب"),
        ('A', "عامل"),
        ('H', "فخرى"),
    )
    membership_type = models.CharField("نوع العضوية", max_length = 1, choices = MEMBERSHIP_TYPE)
    create_date = models.DateField("تحريرا فى", auto_now_add = True)
    modified_date = models.DateField("تاريخ التعديل", auto_now = True)
    personal_image = models.ImageField("صورة شخصية", upload_to = '/image', blank = True, null= True)
    membership_id = models.AutoField("رقم العضوية", primary_key = True)

    def __unicode__(self):
        return str(self.membership_id)

    

class Receipt(models.Model):
    member = models.ForeignKey("رقم العضوية", Member)
    rec_number = models.AutoField("رقم الإيصال", primary_key = True)
    REC_TYPE = (
        ('Y', "رسوم أشتراك سنوية"),
        ('P', "رسوم أشتراك العضوية"),
    )
    rec_type = models.CharField("نوع الإيصال", max_length = 1, choices = REC_TYPE)
    current_date = models.DateField("التاريخ", auto_now_add = True)
    number_of_years = models.IntegerField("عدد السنين مستحقة الدفع", default = 1, blank = True, null = True)
    last_paid_year = models.IntegerField("من", blank = True, null = True)
    current_year = models.IntegerField("إلى", default = date.today().year, blank = True, null = True)

    def __unicode__(self):
        return str(self.rec_number)

    
    

