#!/usr/bin/python
# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def soltan_login(request):
 if request.method == 'POST':
  user = authenticate(username = request.POST['username'], password = request.POST['password'])
 else:
  user = request.user
 if user is not None:
  if user.is_active:
   login(request, user)
   messages.success(request, 'تم تسجيل الدخول بنجاح',)
  else:
   messages.error(request, 'هذا الحساب قد يكون غير مفعل',)
 else:
  messages.error(request, 'تاكد من أسم المستخدم او رمز المرور',)
 return redirect('/')

def soltan_logout(request):
 logout(request)
 messages.success(request, 'تم تسجيل الخروج بنجاح',)
 return redirect('/')

