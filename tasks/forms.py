from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Category, Task


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "username": "Choose a username",
            "email": "Email address",
            "password1": "Create a password",
            "password2": "Confirm password",
        }
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "field-input",
                    "placeholder": placeholders.get(field_name, ""),
                }
            )
        self.fields["password1"].help_text = (
            "8+ characters. Avoid common passwords or all-numeric ones."
        )
        self.fields["password2"].help_text = ""


class TaskForm(forms.ModelForm):
    new_category = forms.CharField(
        required=False,
        label="New category",
        widget=forms.TextInput(
            attrs={"class": "field-input", "placeholder": "Or type a new category"}
        ),
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "category",
            "priority",
            "due_at",
            "is_completed",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "field-input", "placeholder": "Enter task title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "field-input",
                    "placeholder": "Enter description (optional)",
                    "rows": 4,
                }
            ),
            "category": forms.Select(attrs={"class": "field-input"}),
            "priority": forms.Select(attrs={"class": "field-input"}),
            "due_at": forms.DateTimeInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "dd-mm-yyyy --:--",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "is_completed": forms.CheckboxInput(attrs={"class": "field-checkbox"}),
        }
        labels = {
            "is_completed": "Mark as completed",
            "due_at": "Due date & time",
        }

    def __init__(self, *args, owner=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = owner
        if owner is not None:
            self.fields["category"].queryset = Category.objects.filter(owner=owner)
        self.fields["category"].required = False
        self.fields["category"].empty_label = "No category"

    def save(self, commit=True):
        task = super().save(commit=False)
        new_category_name = self.cleaned_data.get("new_category", "").strip()
        if new_category_name and self.owner is not None:
            category, _ = Category.objects.get_or_create(
                owner=self.owner, name=new_category_name
            )
            task.category = category
        if commit:
            task.save()
        return task


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "field-input", "placeholder": "Category name"}
            ),
        }
