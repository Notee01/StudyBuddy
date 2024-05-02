# In your forms.py within the 'courses' app
from django import forms

class FeedbackForm(forms.Form):
    # Define your feedback form fields here
    feedback = forms.CharField(label='Feedback', widget=forms.Textarea)
    # Add more fields as needed
