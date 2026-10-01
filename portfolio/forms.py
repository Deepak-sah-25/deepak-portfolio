from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Invisible honeypot trap to catch automated spam bots
    hp_company = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "tabindex": "-1",
                "style": "display:none !important; position:absolute; left:-9999px;",
            }
        ),
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control-custom",
                    "placeholder": "Your Name",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control-custom",
                    "placeholder": "Your Email Address",
                    "required": True,
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control-custom",
                    "placeholder": "Subject / Project Scope",
                    "required": False,
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control-custom",
                    "rows": 5,
                    "placeholder": "Tell me about your project, goals, or requirements...",
                    "required": True,
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        if self.data.get("hp_company"):
            raise forms.ValidationError("Spam submission detected.")
        return cleaned_data
