from django import forms
from django.utils.translation import ugettext_lazy as _

from userena.forms import SignupForm

class SignupFormExtra(SignupForm):
	first_name = forms.CharField(label = _(u'First name'),
				     max_length =30,
				     required=False)
	last_name = forms.CharField(label = _(u'Last name'),
				     max_length = 30,
				     required=False)
	mobile_number = forms.IntegerField(label = _(u'Mobile number'),
					  max_value =9999999999,
					  required=False)
	def __init__(self, *args, **kw):
		super(SignupFormExtra, self).__init__(*args, **kw)
		new_order = self.fields.keyOrder[:-3]
		new_order.insert(0, 'first_name')
		new_order.insert(1, 'last_name')
		new_order.insert(2, 'mobile_number')
		self.fields.KeyOrder = new_order
	def save(self):
		new_user = super(SignupFormExtra, self).save()
		new_user.first_name = self.cleaned_data['first_name']
		new_user.last_name = self.cleaned_data['last_name']
		new_user.mobile_number = self.cleaned_data['mobile_number']
		new_user.save()
		return new_user()	
