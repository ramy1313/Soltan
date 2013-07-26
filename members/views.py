# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
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
from django.db.models import Max


def index(request):
	if request.user.is_anonymous():
		return redirect('/')
	deactive = False
	since = 0
	if request.GET.get('deactive'):
		members_list = Member.objects.all().exclude(deactivated=False)
		deactive = True
	elif request.GET.get('since'):
		members_list = Member.objects.select_related().exclude(deactivated=True).annotate(last_pyear=Max('receipt__current_date')).filter(last_pyear__lte=request.GET['since']+'-12-31 23:59:59').order_by('-receipt__current_date')
		since = request.GET.get('since')
	else:
		members_list = Member.objects.all().exclude(deactivated=True)
	paginator = Paginator(members_list, 5)
	n = members_list.count
	page = request.GET.get('page')
	try:
		members_list_page = paginator.page(page)
	except PageNotAnInteger:
		members_list_page = paginator.page(1)
	except EmptyPage:
		members_list_page = paginator.page(paginator.num_pages)
	return render(request, 'members/index.html', {'members_list': members_list_page, 'mcount': n, 'now': timezone.now().year, 'deactive': deactive, 'loop_times': [-i for i in range(1,11)], 'since': since})

def detail(request, member_id):
	if request.user.is_anonymous():
		return redirect('/')
	m = get_object_or_404(Member, pk = member_id)
	last_paid = m.get_last_paid()
	return render(request, 'members/detail.html', {'member': m, 'last_paid': last_paid, 'now': timezone.now().year,})

def print_member(request, member_id):
	if request.user.is_anonymous():
		return redirect('/')
	m = get_object_or_404(Member, pk = member_id)
	return render(request, 'members/print_member.html', {'member': m,})

def add_member(request):
	if request.user.is_anonymous():
		return redirect('/')
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
	if request.user.is_anonymous():
		return redirect('/')
	if request.method == 'POST' and 'checkpass' in request.POST:
		if not request.user.check_password(request.POST['password']):
			messages.error(request, 'Profile details deactivated.',)
			return redirect('/')
	member_before_edit = get_object_or_404(Member, pk = member_id)
	if request.method == 'POST' and 'memForm' in request.POST:
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
	if request.user.is_anonymous():
		return redirect('/')
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
	if request.user.is_anonymous():
		return redirect('/')
	m = get_object_or_404(Member, pk = member_id)
	m.deactivated = True
	m.save()
	messages.success(request, 'Profile details deactivated.',)
	return HttpResponseRedirect(reverse('members.views.detail', args=(member_id,)))

def delete_member(request, member_id):
	if request.user.is_anonymous():
		messages.error(request, 'Profile details deactivated.',)
		return redirect('/')
	if request.method == 'POST':
		if not request.user.check_password(request.POST['password']):
			messages.error(request, 'Profile details deactivated.',)
			return redirect('/')
	m = get_object_or_404(Member, pk = member_id)
	m.delete()
	messages.success(request, 'deleted.',)
	return redirect('/')


