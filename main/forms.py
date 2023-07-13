from django import forms

from main.models import SendingSettings, Message, Log, Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'description']


class SendingSettingsForm(forms.ModelForm):
    class Meta:
        model = SendingSettings
        fields = ['subject', 'body', 'frequency', 'status', 'customers']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = '__all__'
