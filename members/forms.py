from members.models import Member, Receipt
from django.forms import ModelForm

class MemberForm(ModelForm):
	class Meta:
		model = Member
		fields = ['name', 'job', 'membership_id', 'birth_date', 'birth_place', 'membership_type', 'address', 'national_number', 'tel', 'mobile']

