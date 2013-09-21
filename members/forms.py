#!/usr/bin/python
# -*- coding: utf-8 -*-
from members.models import Member, Receipt, MemberFees
from django.forms import ModelForm, Form
from django.forms.fields import TextInput
from django.forms.forms import BoundField
from django.forms.widgets import HiddenInput
from django import forms 


class MemberForm(ModelForm):
	memForm = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
	class Meta:
		model = Member
		fields = ['name', 'membership_id', 'membership_type', 'address', 'national_number', 'job', 'birth_date', 'birth_place', 'tel', 'mobile', 'personal_image']
		widgets = {
			'birth_date': forms.DateInput(format='%Y-%m-%d', attrs={'class':'datePicker', 'readonly':'true'}),
		}
		

	def save(self, commit = True):
		m = super(MemberForm, self).save(commit = False)
		if commit:
			m.save()
		if m.get_last_paid() == 1:
			m.receipt_set.create(rec_type = 'P')
			m.receipt_set.create(rec_type = 'Y', number_of_years= 1)
		return m


class ReceiptForm(ModelForm):
	amount = forms.IntegerField(label = "المبلغ المطلوب", widget=forms.HiddenInput())
	class Meta:
		model = Receipt
		fields = ['member', 'rec_number', 'number_of_years', 'last_paid_year']

	def __init__(self, *args, **kwargs):
		super(ReceiptForm, self).__init__(*args, **kwargs)
		self.fields['member'].widget = HiddenInput()
		self.fields['member'].label = "رقم العضو"
		self.fields['last_paid_year'].widget = HiddenInput()
		self.fields['number_of_years'].widget = HiddenInput()
		

	def save(self, commit = True):
		r = super(ReceiptForm, self).save(commit = False)
		r.rec_type = 'Y'
		if commit:
			r.save()
		return r

class MemberFeeForm(ModelForm):
	password = forms.CharField(label = "رمز المرور", widget=forms.PasswordInput())
	class Meta:
		model = MemberFees
		fields = ['regestration_fee', 'year_fee']

	def save(self, commit = True):
		f = super(MemberFeeForm, self).save(commit = False)
		MemberFees.objects.all().delete()
		if commit:
			f.save()
		return f

class MemberSearchForm(Form):
	membersearch = forms.IntegerField(label = "رقم العضوية")

class RecSearchForm(Form):
	recsearch = forms.IntegerField(label = "رقم الإيصال")
		

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
