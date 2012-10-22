from django import forms
from django.utils.translation import ugettext_lazy as _

from userena.forms import SignupForm
from users.models import UserProfile

class SignupFormExtra(SignupForm):
	#first_name = forms.CharField(label = _(u'First name'),
	#			     max_length =30,
	#			     required=False)
	#last_name = forms.CharField(label = _(u'Last name'),
	#			     max_length = 30,
	#			     required=False)
	mobile_number = forms.CharField(label = _(u'mobile number'),
					  max_length =10,
					  required=True)
#	def __init__(self, *args, **kw):
#		super(SignupFormExtra, self).__init__(*args, **kw)
#		new_order = self.fields.keyOrder[:-3]
#		new_order.insert(0, 'first_name')
#		new_order.insert(1, 'last_name')
#		new_order.insert(2, 'mobile_number')
#		self.fields.KeyOrder = new_order
	def save(self):
		new_user= super(SignupFormExtra, self).save()
		user_profile = new_user.get_profile()
		#user_profile.first_name = self.cleaned_data['first_name']
		#user_profile.last_name = self.cleaned_data['last_name']
		user_profile.mobile_number = self.cleaned_data['mobile_number']
		#user_profile.mobile_number = UserProfile.objects.get_or_create(name=user_profile.mobile_number)

		user_profile.save()
		return new_user	
