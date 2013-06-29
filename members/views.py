# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, render
from members.models import Member, Receipt
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from members.forms import MemberForm, ReceiptForm
from soltan import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib import messages


def index(request):
	members_list = Member.objects.all().order_by('-create_date')
	paginator = Paginator(members_list, 5)
	n = members_list.count
	page = request.GET.get('page')
	try:
		members_list_page = paginator.page(page)
	except PageNotAnInteger:
		members_list_page = paginator.page(1)
	except EmptyPage:
		members_list_page = paginator.page(paginator.num_pages)
	return render(request, 'members/index.html', {'members_list': members_list_page, 'mcount': n, 'now': timezone.now().year})

def detail(request, member_id):
	m = get_object_or_404(Member, pk = member_id)
	last_paid = m.get_last_paid()
	return render(request, 'members/detail.html', {'member': m, 'last_paid': last_paid, 'now': timezone.now().year,})

def print_member(request, member_id):
	m = get_object_or_404(Member, pk = member_id)
	return render(request, 'members/print_member.html', {'member': m,})

def add_member(request):
	if request.method == 'POST':
		form = MemberForm(request.POST, request.FILES)
		if form.is_valid():
			m = form.save()
			messages.success(request, 'Profile details updated.', extra_tags = 'printDia')
			return HttpResponseRedirect(reverse('members.views.detail', kwargs={'member_id': m.membership_id,}))
	else:
		form = MemberForm()
	return render(request, 'members/add_member.html', {
        'form': form,
    })

def edit_member(request, member_id):
	member_before_edit = get_object_or_404(Member, pk = member_id)
	if request.method == 'POST':
		form = MemberForm(request.POST, request.FILES, instance = member_before_edit)
		if form.is_valid():
			m = form.save()
			messages.success(request, 'Profile details updated.',)
			return HttpResponseRedirect(reverse('members.views.detail', kwargs={'member_id': m.membership_id,}))
	else:
		form = MemberForm(instance = member_before_edit)
	return render(request, 'members/add_member.html', {
        'form': form,
        'member_id': member_id,
        'edit': True
    })

def pay_receipt(request, membership_id):
	if request.method == 'POST':
		form = ReceiptForm(request.POST)
		if form.is_valid():
			r = form.save()
			return HttpResponseRedirect(reverse('members.views.detail', args=(membership_id,)))
	else:
		m = get_object_or_404(Member, pk = membership_id)
		l = m.get_last_paid()
		if l == 0 or l == 1:
			l = timezone.now().year
		n = timezone.now().year - l
		form = ReceiptForm({'member': membership_id, 'last_paid_year': l, 'number_of_years': n})
	return render(request, 'members/pay_receipt.html', {
        'form': form,
        'membership_id': membership_id,
    })

def deactivate(request, member_id):
	pass

def soltan_login(request):
	pass
