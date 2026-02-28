from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Topics

User = get_user_model()

#=========================
#=== For Creating User ===
#=========================
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email'
        })

        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password'
        })

        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Password for confirmation'
        })

#===========================
#=== For Posting Article ===
#===========================
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class PostArticleForm(forms.Form):
    title = forms.CharField(max_length=512)
    genre = forms.ModelChoiceField(Topics.objects.all())
    summary = forms.CharField(max_length=500, widget=forms.Textarea)
    html_file = MultipleFileField(widget=MultipleFileInput(attrs={'webkitdirectory':''}))
    is_limited = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class':'form-check-input'}),
        required=False
    )


