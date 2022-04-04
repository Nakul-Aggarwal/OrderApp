from django import forms

class CartForm(forms.Form):

    starter = forms.BooleanField()
    description = forms.CharField(max_length=1000, required = False)
