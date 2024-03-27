from django import forms
from .models import ChocolateyPackage

class InstallForm(forms.Form):
    packages = forms.ModelMultipleChoiceField(queryset=ChocolateyPackage.objects.all(), widget=forms.CheckboxSelectMultiple)