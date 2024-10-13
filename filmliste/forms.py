from django import forms

class NameForm(forms.Form):
  test = forms.CharField(label="lol", max_length=100)