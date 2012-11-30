from django.forms import ModelForm
from accounts.models import MyProfile

class MugshotForm(ModelForm):
	class Meta:
		model = MyProfile
		fields = ('mugshot', )