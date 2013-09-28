#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from datetime import date
from django.core import validators

# Create your models here.

class Person(models.Model):
	"""docstring for Person"""
	N_ID = models.CharField("اﻟﺮﻗﻢ اﻟﻘﻮﻣﻰ", max_length = 14, validators = [validators.RegexValidator(r'^[0-9]*$', 'يسمح فقط بالأرقام من 0-9', 'Invalid Number'), validators.MinLengthValidator(14)], primary_key = True)
	name = models.CharField("الأسم", max_length = 200)
	GENDER = (
		('M', "ذكر"),
		('F', "أنثى"),
	)
	gender = models.CharField("الجنس", max_length = 1, choices = GENDER, blank = False, null = False)
	birth_date = models.DateField("ﺗﺎﺭﻳﺦ اﻟﻤﻴﻼﺩ")
	create_date = models.DateField("تاريخ التسجيل بقاعده البيانات", auto_now_add = True)
	notes = models.TextField("ملاحظات", null = True, blank = True)
	student = models.BooleanField("طالب", default = False)
	grade = models.CharField("السنة الدراسية", max_length = 50, null = True, blank = True)
	HEALTH_STATUS = (
		('G', "جيدة"),
		('E', "مرض مزمن"),
		('D', "عجز ونسبته"),
		('O', "أمراض الشيخوخة"),
		('H', "إعاقة"),
		('A', "أخرى"),
	)
	health_status = models.CharField("الحالة الصحية", max_length = 1, choices = HEALTH_STATUS, blank = False, null = False, default = 'G')
	health_note = models.TextField("ملاحظات عن الحالة الصحية", null = True, blank = True)

	def __unicode__(self):
		return str(self.name)

class Cases(models.Model):
    """docstring for Cases"""
    permanent_ID = models.AutoField("الرقم الدائم للحالة", primary_key = True)
    record_ID = models.IntegerField("الرقم فى السجلات", unique = True, null = True, blank = True)
    file_number = models.IntegerField("رقم السجل", null = True, blank = True)
    address = models.CharField("اﻟﻌﻨﻮاﻥ", max_length = 100)
    tel = models.CharField("اﻟﺘﻠﻴﻔﻮﻥ", max_length = 25, blank = True, validators = [validators.RegexValidator(r'^\+?[0-9]*$', 'يسمح فقط بالأرقام من 0-9 أو +', 'Invalid Number'), validators.MinLengthValidator(7)])
    mobile = models.CharField("ﻣﺤﻤﻮﻝ", max_length = 25, blank = True, validators = [validators.RegexValidator(r'^\+?[0-9]*$', 'يسمح فقط بالأرقام من 0-9 أو +', 'Invalid Number'), validators.MinLengthValidator(7)])
    monthly_income_value = models.FloatField("الدخل الشهرى", null = True, blank = True)
    monthly_income_source = models.CharField("مصدر الدخل الشهرى", max_length = 50, null = True, blank = True)
    another_sources = models.TextField("جمعيات أخرى معاونة", null = True, blank = True)
    MATERIAL_STATUS = (
    	('W', "أرملة"),
    	('D', "مطلق"),
    	('S', "أعزب"),
    	('N', "أنسة"),
    	('M', "متزوج ويعول"),
    )
    material_status = models.CharField("الحالة الأجتماعية", max_length = 1, choices = MATERIAL_STATUS, blank = False, null = False)
    case_date = models.DateField("تاريخ تسجيل الحالة")
    create_date = models.DateField("تاريخ التسجيل بقاعده البيانات", auto_now_add = True)
    HOUSE = (
    	('O', "تمليك"),
    	('R', "إيجار"),
    	('N', "إيجار جديث"),
    	('C', "مشترك"),
    	('F', "مع العائلة"),
    )
    house = models.CharField("السكن", max_length = 1, choices = HOUSE)
    house_value = models.FloatField("قيمته المنزل", null = True, blank = True)
    house_rooms = models.IntegerField("عدد الحجرات", null = True, blank = True, default = 0)
    house_desc = models.TextField("وصف السكن", null = True, blank = True)
    food_bank_code = models.CharField("كود بنك الطعام", max_length = 10, null = True, blank = True)
    gov_supply = models.BooleanField("التموين الحكومى")
    supply_numbers = models.IntegerField("عدد الافراد فى بطاقة التموين", null = True, blank = True, default = 0)
    supply_card = models.CharField("رقم بطاقة التموين", max_length = 25, null = True, blank = True)
    notes = models.TextField("ملاحظات", null = True, blank = True)
    CASE_TYPE = (
    	('A', "أعانة"),
    	('B', "كفالة"),
    	('C', "عينى"),
    )
    case_type = models.CharField("نوع الحالة", max_length = 1, choices = CASE_TYPE)
    deactivated = models.BooleanField("غير مفعل", default = False)
    case_owner = models.ForeignKey(Person, verbose_name = "الرقم القومى لصاحب البحث")

    def __unicode__(self):
    	return Person.objects.get(pk = self.case_owner)

class CaseMembers(models.Model):
    case_id = models.ForeignKey(Cases, verbose_name = "الحالة")
    person_id = models.ForeignKey(Person, verbose_name = "الشخص")
    REL = (
    	('P', "زوج/زوجة"),
        ('B', "أبن/أبنه"),
    )
    rel = models.CharField("العلاقة", max_length = 1, choices = REL)
    unregistered = models.BooleanField("حذف من الحالة", default = False)
    date_of_unvoke = models.DateField("تاريخ حذف العلاقة", null = True, blank = True)

class Disbursements(models.Model):
    case_id = models.ForeignKey(Cases, verbose_name = "الحالة")
    child_name = models.CharField("أسم الطفل", max_length = 100)
    exchange_date = models.DateField("تاريخ الصرف")
    ITEMS = (
        ('A', "أعانات مالية"),
        ('B', "لحوم"),
        ('C', "كرتونة رمضان"),
        ('D', "مواد غذائية"),
        ('E', "ملابس عيد"),
        ('F', "أحذية"),
        ('G', "ملابس مدارس"),
        ('H', "أدوات مدارس"),
        ('I', "أدوية"),
        ('J', "أعانات زواج"),
        ('K', "أعانات تعليم جامعه"),
    )
    items = models.CharField("الأصناف المنصرفة", max_length = 1, choices = ITEMS)
    quantity = models.FloatField("الكمية")
    notes = models.TextField("ملاحظات")

    def __unicode__(self):
        return str(self.id)

