
from django import forms
from django.forms.widgets import SelectDateWidget
from datetime import datetime, date
from django.forms import DateInput, DateTimeInput, ModelForm
from .models import Dataset, User, CompetitionSolution
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
# from django.contrib.auth.models import User



class CompetitionForm(forms.Form):
    competition_name = forms.CharField(max_length=255)
    # competition_banner_upload = forms.ImageField(required=False)
    # competition_rules = forms.CharField(widget=forms.Textarea)
    competition_description = forms.CharField(widget=forms.Textarea)
    competition_prize = forms.DecimalField(min_value=1)


     # Add the fields from datasetsForm
    dataset_name = forms.CharField(max_length=255, required=True)
    dataset_description = forms.CharField(widget=forms.Textarea, required=True)
    dataset_file = forms.FileField()


    categories = forms.ChoiceField(choices=[('public', 'Public'), ('economic', 'Economic'), ('finance', 'Finance'), ('technology', 'Technology'), ('sports', 'Sports'), ('custom', 'Custom')], widget=forms.RadioSelect)
    start_date = forms.DateTimeField(widget=DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateTimeField(widget=DateInput(attrs={'type': 'date'}), required=False)
    premium = forms.BooleanField(required=False,  widget=forms.CheckboxInput(attrs={'class': 'premium-checkbox'}))

    # Updated the indentation to match the class level
    def __init__(self, *args, **kwargs):
        features = kwargs.pop('features', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if 'competition_name' in cleaned_data and not cleaned_data['competition_name'].replace(' ', '').isalnum():
            raise forms.ValidationError('Competition name can only contain letters, numbers, and spaces')

        today = timezone.now().date()

        if start_date and start_date.date() < today:
            self.add_error('start_date', 'Start date cannot be before today')
        
        if end_date and end_date.date() < today:
            self.add_error('end_date', 'End date cannot be before today')
        
        if start_date and end_date and start_date > end_date:
            self.add_error('start_date', 'Start date cannot be after end date')
            self.add_error('end_date', 'End date cannot be before start date')

        return cleaned_data

class DatasetForm(forms.ModelForm):
    file = forms.FileField()
    
    class Meta:
        model = Dataset
        fields = ['name', 'description']
        labels = {
            'name': 'Dataset name',
            'description': 'Description',
            'file': 'File',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

class SolutionForm(forms.ModelForm):
    file = forms.FileField()
    
    class Meta:
        model = CompetitionSolution
        fields = ['name']
        labels = {
            'name': 'Solution name',
            'file': 'File',
        }
        # widgets = {
        #     'description': forms.Textarea(attrs={'rows': 5}),
        # }

class RegistrationForm(UserCreationForm):
    first_name =  forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    university = forms.CharField(max_length=100, required=False)
    company = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'phone_number', 'university', 'company']