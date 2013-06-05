# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, render
from members.models import Member, Receipt
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from members.forms import MemberForm
from soltan import settings

def index(request):
	members_list = Member.objects.all().order_by('-create_date')
	return render_to_response('members/index.html', {'members_list': members_list})

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
