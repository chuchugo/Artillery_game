from django import forms

class ShootForm(forms.Form):
    angle = forms.FloatField(max_value=90, min_value=0)
    velocity = forms.FloatField(max_value=100, min_value=0)
