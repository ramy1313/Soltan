#!/usr/bin/python
# -*- coding: utf-8 -*-
# Create your views here.

from cases.models import *
from cases.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse

def add_case(request):
	if request.user.is_anonymous():
		messages.error(request, 'عفوا لايمكن دخول الصفحة إلا إذا كنت مسجل',)
		return redirect('/')
	relatives_formset = formset_factory(CaseRelativeForm, formset = BaseRelativeFormset)
	if request.method == 'POST':
		reltiveFormset = relatives_formset(request.POST, request.FILES, prefix = "reltive")
		caseowner = MainCaseOwner(request.POST, request.FILES, prefix = "owner")
		case = CaseForm(request.POST, request.FILES, prefix = "case")
		zone = ZoneForm(request.POST, request.FILES, prefix = "zone")
		if reltiveFormset.is_valid() and caseowner.is_valid() and case.is_valid():
			o = caseowner.save()
			c = case.save(caseowner_id = o)
			reltiveFormset.save(ccase_id = c)
			messages.success(request, 'تم أضافة العضو بنجاح', extra_tags = 'printDia')
			return HttpResponseRedirect(reverse('cases.views.detail', kwargs={'case_id': c.permanent_ID,}))
	else:
		reltiveFormset = relatives_formset(prefix = "reltive")
		caseowner = MainCaseOwner(prefix = "owner")
		case = CaseForm(prefix = "case")
		zone = ZoneForm(prefix = "zone")
	return render(request, 'cases/add_case.html', {
        'reltiveFormset': reltiveFormset,
        'caseowner': caseowner,
        'case': case,
        'zone': zone,
    })

def detail(request, case_id):
	if request.user.is_anonymous():
		messages.error(request, 'عفوا لايمكن دخول الصفحة إلا إذا كنت مسجل',)
		return redirect('/')
	return render(request, 'cases/details.html')
