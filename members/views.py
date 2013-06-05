# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, render
from members.models import Member, Receipt
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from members.forms import MemberForm, ReceiptForm
from soltan import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
	return render_to_response('members/index.html', {'members_list': members_list_page, 'mcount': n})

def detail(request, member_id):
	m = get_object_or_404(Member, pk = member_id)
	last_paid = m.get_last_paid()
	return render_to_response('members/detail.html', {'member': m, 'last_paid': last_paid})

def print_member(request, member_id):
	m = get_object_or_404(Member, pk = member_id)
	return render_to_response('members/print_member.html', {'member': m, 'MEDIA_URL': settings.MEDIA_URL})

def add_member(request):
	if request.method == 'POST':
		form = MemberForm(request.POST, request.FILES)
		if form.is_valid():
			m = form.save()
			return HttpResponseRedirect(reverse('members.views.print_member', args=(m.membership_id,)))
	else:
		form = MemberForm()
	return render(request, 'members/add_member.html', {
        'form': form,
    })

def pay_receipt(request, membership_id):
	if request.method == 'POST':
		form = ReceiptForm(request.POST)
		if form.is_valid():
			r = form.save()
			return HttpResponseRedirect(reverse('members.views.add_member', args=(membership_id,)))
	else:
		form = ReceiptForm({'member': membership_id, 'rec_type': 'Y'})
	return render(request, 'members/pay_receipt.html', {
        'form': form,
        'membership_id': membership_id,
    })
