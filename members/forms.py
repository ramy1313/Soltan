from members.models import Member, Receipt
from django.forms import ModelForm

class MemberForm(ModelForm):
	class Meta:
		model = Member
		fields = ['name', 'membership_id', 'membership_type', 'address', 'national_number', 'job', 'birth_date', 'birth_place', 'tel', 'mobile', 'personal_image']

