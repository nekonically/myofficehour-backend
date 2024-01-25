from django import forms
from Myofficehour.models import Participant

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['id',"email"]
        widgets = {
            'id': forms.HiddenInput(),  # This makes the 'id' field hidden
            'email':forms.EmailInput(attrs={ 'placeholder' : 'email address'})
        }