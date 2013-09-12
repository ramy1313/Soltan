#!/usr/bin/python
# -*- coding: utf-8 -*-
# Create your views here.

from cases.models import *
from cases.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.forms.models import modelformset_factory
