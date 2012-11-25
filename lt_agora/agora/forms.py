from django import forms

from agora.models import Decision

class DecisionForm(forms.ModelForm):

	class Meta:
		model = Decision