
from django import forms
from .models import stateNames,allergenlist


class RecipeFormGuest(forms.Form):
    
    SelectedState = forms.ModelChoiceField(queryset=stateNames.objects.all(), label='Select a state',required=False)
    SelectedAllergen=forms.ModelMultipleChoiceField(queryset=allergenlist.objects.all(),widget=forms.CheckboxSelectMultiple, label="Select the allergies",required=False)

class RecipeFormUser(forms.Form):
    
    SelectedState = forms.ModelChoiceField(queryset=stateNames.objects.all(), label='Select a state',required=False)
   
class AllergenForm(forms.Form):

    SelectedAllergen=forms.ModelMultipleChoiceField(queryset=allergenlist.objects.all(),widget=forms.CheckboxSelectMultiple, label="Select the allergies",required=False)
