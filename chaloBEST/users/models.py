from django.db import models
from django.contrib.auth.models import User
from userena.models import UserenaBaseProfile
from userena.models import UserenaLanguageBaseProfile
#from django.contrib.auth.models import User
#from django.contrib.auth.models import User
#from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
import datetime

# Create your models here.
class UserProfile(UserenaLanguageBaseProfile):
	GENDER_CHOICES =(
		(1, _('Male')),
		(2, _('Female')),
	)

#	user = models.ForeignKey(User, unique=True)
#	url - models.URLField("Website", blank=True)
#	company = models.CharField(max_length=50, blank=True)
	user =  models.ForeignKey(User,
				    unique=True,
				    verbose_name =('user'),
				    related_name = 'profile')
	gender = models.PositiveSmallIntegerField(_('gender'),
						 choices=GENDER_CHOICES,
						 blank = True,
						null=True)
	website = models.URLField(_('website'), blank=True, verify_exists=True)
	location = models.CharField(_('location'), max_length=255, blank=True)
	birth_date = models.DateField(_('birth date'), blank=True, null=True)
#	about_me = models.TextField(_('about me'), blank = True)
	mobile_number = models.CharField(_('mobile number'), blank = True, max_length=10)
	about_me = models.TextField(_('about me'), blank = True)

	@property
	def age(self):
		if not self.birth_date: return False
		else:
			today = datetime.date.today()
			try:
				birthday = self.birth_date.replace(year=today.year)
			except ValueError:
				day = today.day -1 if today.day != 1 else today.day + 2
				birthday = self.birth_date.replace(year=today.year, day = day)
			if birthday > today: return today.year - self.birth_date.year - 1
			else: return today.year - self.birth_date.year
#def create_user_profile(sender, instance, created, **kwargs):
#	if created:
#		UserProfile.objects.create(user=instance)

#post_save.connect(create_user_profile, sender=User)
#def create_profile(sender, **kw):
#	user = kw["instance"]
#	if kw["created"]:
#		up = UserProfile(user=user, gender=1,location="test")
#		up.save()
#post_save.connect(create_profile, sender=User)


#User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

