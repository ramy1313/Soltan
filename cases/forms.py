#!/usr/bin/python
# -*- coding: utf-8 -*-
from cases.models import *
from django.forms import ModelForm, Form, ChoiceField, Select, CharField, DateInput
from django.forms.forms import BoundField


class MainCaseOwner(ModelForm):
    class Meta:
        model = Person
        fields = ['N_ID', 'name', 'gender', 'birth_date', 'notes', 'student', 'grade', 'health_status', 'health_note']
        widgets = {
            'birth_date': DateInput(format='%Y-%m-%d', attrs={'class':'datePicker', 'readonly':'true'}),
        }

class CaseForm(ModelForm):
    class Meta:
        model = Cases
        fields = ['case_type', 'material_status', 'record_ID', 'file_number', 'address', 'tel', 'mobile', 'monthly_income_value', 'monthly_income_source', 'another_sources', 'case_date', 'house', 'house_value', 'house_rooms', 'house_desc', 'food_bank_code', 'gov_supply', 'supply_numbers', 'supply_card', 'notes']
        widgets = {
            'case_date': DateInput(format='%Y-%m-%d', attrs={'class':'datePicker', 'readonly':'true'}),
        }

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
    zones = CharField("المنطقة", widget=Select(choices=ZONES))
	#zones = ChoiceField("المنطقة", widget = Select(choices = ZONES))# choices = ZONES)

class CaseRelativeForm(MainCaseOwner):
    REL = (
    	('P', "زوج/زوجة"),
        ('B', "أبن/أبنه"),
    )
    rela = CharField("العلاقة", widget=Select(choices=REL))
    #rela = ChoiceField("العلاقة", widget = Select(choices = REL))

    def save(self, ccase_id = None, relat = None, commit = True):
    	r = super(CaseRelativeForm, self).save(commit = False)
    	if commit:
    		r.save()
    	relat = self.cleaned_data['rela']
    	re = CaseMembers(case_id = ccase_id, person_id = r.N_ID, rel = relat)
    	return r


def decorate_label_tag(f):
 
    def bootstrap_label_tag(self, contents=None, attrs=None):
        attrs = attrs or {}
        add_class(attrs, 'control-label')
        return f(self, contents, attrs)
 
    return bootstrap_label_tag
 
 
BoundField.label_tag = decorate_label_tag(
         BoundField.label_tag)
 
 
def add_class(attrs, html_class):
    assert type(attrs) is dict
 
    if 'class' in attrs:
        classes = attrs['class'].split()
        if not html_class in classes:
            classes.append(html_class)
            attrs['class'] = ' '.join(classes)
    else:
        attrs['class'] = html_class
