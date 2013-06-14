from members.models import Member, Receipt
from django.forms import ModelForm
from django.forms.fields import TextInput

class MemberForm(ModelForm):
	class Meta:
		model = Member
		fields = ['name', 'membership_id', 'membership_type', 'address', 'national_number', 'job', 'birth_date', 'birth_place', 'tel', 'mobile', 'personal_image']

	def save(self, commit = True):
		m = super(MemberForm, self).save(commit = False)
		if commit:
			m.save()
		m.receipt_set.create(rec_type = 'P')
		m.receipt_set.create(rec_type = 'Y', number_of_years= 1)
		return m


class ReceiptForm(ModelForm):
	class Meta:
		model = Receipt
		fields = ['member', 'rec_number','number_of_years', 'last_paid_year']

	def __init__(self, *args, **kwargs):
		super(ReceiptForm, self).__init__(*args, **kwargs)
		self.fields['member'].widget = TextInput(attrs={'size':'10'})
		self.fields['member'].widget.attrs['readonly'] = True
		self.fields['last_paid_year'].widget.attrs['readonly'] = True
		self.fields['number_of_years'].widget.attrs['readonly'] = True
		

	def save(self, commit = True):
		r = super(ReceiptForm, self).save(commit = False)
		r.rec_type = 'Y'
		if commit:
			r.save()
		return r
		

