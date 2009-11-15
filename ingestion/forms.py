from django import forms
from models import *

class LayerAddForm(forms.ModelForm):
    class Meta:
        model = Layer


class Source(forms.ModelForm):
    class Meta:
        model = Source
        