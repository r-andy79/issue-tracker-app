from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ('ticket_type', 'title', 'text')


class UserLoginForm(forms.Form):
    """Form to be used to log users in"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)