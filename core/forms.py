from django import forms

from .models import ContactSubmission


class ContactSubmissionForm(forms.ModelForm):
    # Honeypot field: invisible to visitors and not persisted.
    website = forms.CharField(required=False, widget=forms.HiddenInput)
    inquiry_type = forms.ChoiceField(
        choices=[("", "Select a category"), *ContactSubmission.InquiryType.choices],
        required=True,
        error_messages={"required": "Please select the nature of your inquiry."},
    )

    class Meta:
        model = ContactSubmission
        fields = ["full_name", "organization", "email", "inquiry_type", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name", "required": True}),
            "organization": forms.TextInput(attrs={"placeholder": "Fund, firm, or institution", "autocomplete": "organization"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@company.com", "autocomplete": "email", "required": True}),
            "inquiry_type": forms.Select(attrs={"required": True}),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Tell us how you want to move together…",
                    "cols": 20,
                    "rows": 2,
                    "required": True,
                }
            ),
        }
        labels = {
            "full_name": "Full Name",
            "organization": "Organization",
            "email": "Email Address",
            "inquiry_type": "Nature of inquiry",
            "message": "Message",
        }
        error_messages = {
            "full_name": {"required": "Please enter your full name."},
            "email": {
                "required": "Please enter your email address.",
                "invalid": "Please enter a valid email address.",
            },
            "message": {"required": "Please enter your message."},
        }
