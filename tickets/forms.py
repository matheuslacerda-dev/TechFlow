from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Department, Employee, Resolution, Ticket


BASE_INPUT_CLASS = "lb-input"
BASE_SELECT_CLASS = "lb-select"
BASE_TEXTAREA_CLASS = "lb-textarea"


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": BASE_INPUT_CLASS,
                    "placeholder": "Infrastructure",
                }
            ),
            "localization": forms.TextInput(
                attrs={
                    "class": BASE_INPUT_CLASS,
                    "placeholder": "HQ - 3rd Floor",
                }
            ),
            "chief_of_department": forms.TextInput(
                attrs={
                    "class": BASE_INPUT_CLASS,
                    "placeholder": "Morgan Smith",
                }
            ),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["position", "phone_number", "department"]
        widgets = {
            "position": forms.TextInput(
                attrs={
                    "class": BASE_INPUT_CLASS,
                    "placeholder": "Analyst or Technician",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": BASE_INPUT_CLASS,
                    "placeholder": "+1 555 010 000",
                }
            ),
            "department": forms.Select(
                attrs={
                    "class": BASE_SELECT_CLASS,
                }
            ),
        }


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "priority",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": BASE_INPUT_CLASS,
                    "placeholder": "What's happening?",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": BASE_TEXTAREA_CLASS,
                    "rows": 5,
                    "placeholder": "Describe the issue in detail",
                }
            ),
            "priority": forms.RadioSelect(),
        }


class ResolutionForm(forms.ModelForm):
    class Meta:
        model = Resolution
        fields = ["comment", "spent_time"]
        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "class": BASE_TEXTAREA_CLASS,
                    "rows": 4,
                    "placeholder": "Describe root cause, fix, and follow-up actions.",
                }
            ),
            "spent_time": forms.TextInput(
                attrs={
                    "class": BASE_INPUT_CLASS,
                    "placeholder": "HH:MM:SS",
                }
            ),
        }


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": BASE_INPUT_CLASS,
                    "placeholder": "matheus.lacerda",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": BASE_INPUT_CLASS,
                    "placeholder": "name@company.com",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = "Letters, digits and @ . + - _"
        self.fields["email"].widget.attrs.update(
            {
                "class": BASE_INPUT_CLASS,
                "placeholder": "name@company.com",
            }
        )
        self.fields["password1"].help_text = (
            "At least 8 chars. Avoid common or fully numeric passwords."
        )
        self.fields["password2"].help_text = "Type the same password for confirmation."
        self.fields["password1"].widget.attrs.update(
            {
                "class": BASE_INPUT_CLASS,
                "placeholder": "Create password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": BASE_INPUT_CLASS,
                "placeholder": "Confirm password",
            }
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email", "")
        if commit:
            user.save()
        return user
