from django import forms
from .models import Therapist
from .models import Appointment
from .models import ForumTopic, Comment
from django.contrib.auth.forms import AuthenticationForm


class TherapistSearchForm(forms.Form):
    query = forms.CharField(label='Search', required=False, widget=forms.TextInput(attrs={'placeholder': 'Search Therapists'}))


class TherapistForm(forms.ModelForm):
    class Meta:
        model = Therapist
        fields = ['name', 'specialization', 'rating', 'bio', 'fee', 'availability']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['therapist', 'appointment_time']
        widgets = {
            'appointment_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class ForumTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']



from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))