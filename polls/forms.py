# Create this new file: polls/forms.py

from django import forms

class ContactForm(forms.Form):
    """
    A simple contact form.
    Django's Form class automatically handles security features:
    1. Validation: Checks for max_length, required fields, etc.
    2. Sanitization: CharField.to_python() strips leading/trailing whitespace.
    3. Output Escaping: When rendered with {{ form }}, Django escapes it.
    """
    name = forms.CharField(
        label="Your Name",
        max_length=100,
        required=True,
        help_text="Max 100 characters."
    )
    
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea,
        required=False
    )
