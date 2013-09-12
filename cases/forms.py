#!/usr/bin/python
# -*- coding: utf-8 -*-
from cases.models import *
from django.forms import ModelForm, Form, ChoiceField

class MainCaseOwner(ModelForm):
	class Meta:
		model = Person
		fields = ['N_ID', 'name', 'gender', 'birth_date', 'notes', 'student', 'grade', 'health_status', 'health_note']

class CaseForm(ModelForm):
	class Meta:
		model = Cases
		fields = ['case_type', 'material_status', 'record_ID', 'file_number', 'address', 'tel', 'mobile', 'monthly_income_value', 'monthly_income_source', 'another_sources', 'case_date', 'house', 'house_value', 'house_rooms', 'house_desc', 'food_bank_code', 'gov_supply', 'supply_numbers', 'supply_card', 'notes']

	def save(self, caseowner_id = None, commit = True):
		c = super(CaseForm, self).save(commit = False)
		c.case_owner = caseowner_id
		if commit:
			c.save()
		return c

class ZoneForm(Form):
	ZONES = (
		('K', "كرموز"),
		('R', "راتب"),
		('G', "غيط العنب"),
		('O', "أخرى"),
	)
	zones = ChoiceField("المنطقة", choices = ZONES)

class CaseRelativeForm(MainCaseOwner):
	REL = (
    	('P', "زوج/زوجة"),
        ('B', "أبن/أبنه"),
    )
    rela = ChoiceField("العلاقة", choices = REL)

    def save(self, ccase_id = None, relat = None, commit = True):
    	r = super(CaseRelativeForm, self).save(commit = False)
    	if commit:
    		r.save()
    	re = CaseMembers(case_id = ccase_id, person_id = r.N_ID, rel = relat)
    	return r