from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms import ModelForm
from django.contrib.auth.hashers import make_password
from .models import User, Predmeti, Enrollment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=User.ROLES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'status']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }
    
    def clean_role(self):
        role = self.cleaned_data['role']
        if role not in dict(User.ROLES).keys():
            raise forms.ValidationError("Invalid role selection.")
        return role
    
class PredmetiForm(ModelForm):
    class Meta:
        model = Predmeti
        fields = ['Ime','Kod','Program','ECTS','sem_red','sem_izv', 'izborni', 'nositelj']

    def __init__(self, *args, **kwargs):
        super(PredmetiForm, self).__init__(*args, **kwargs)
        # Filter the queryset of the nositelj field to only include professors
        self.fields['nositelj'].queryset = User.objects.filter(role='prof')

class StudentForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        role = cleaned_data.get('role')

        if status is 'None':
            raise forms.ValidationError("Status field cannot be None.")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'status', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'stu'
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class ProfesorForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        role = cleaned_data.get('role')
        status = 'None'
        if role != 'prof':
            raise forms.ValidationError("Role must be 'professor'.")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'username', 'role', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'prof'
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['subject']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  #spremi korisinka
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Predmeti.objects.all()

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if Enrollment.objects.filter(student=self.user, subject=subject).exists():
            raise forms.ValidationError("You are already enrolled in this subject.")
        return subject