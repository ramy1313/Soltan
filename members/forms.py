from members.models import Member, Receipt
from django.forms import ModelForm
from django.forms.fields import TextInput

class MemberForm(ModelForm):
	class Meta:
		model = Member
		fields = ['name', 'membership_id', 'membership_type', 'address', 'national_number', 'job', 'birth_date', 'birth_place', 'tel', 'mobile', 'personal_image']

class ReceiptForm(ModelForm):
	class Meta:
		model = Receipt
		fields = ['member', 'rec_number', 'rec_type','number_of_years', 'last_paid_year']

	def __init__(self, *args, **kwargs):
		super(ReceiptForm, self).__init__(*args, **kwargs)
		self.fields['member'].widget = TextInput(attrs={'size':'10'})
		self.fields['member'].widget.attrs['readonly'] = True
		

