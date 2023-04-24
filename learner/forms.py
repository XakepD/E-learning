from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm,UserChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from . models import *
from django import forms
from django.forms import inlineformset_factory
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('amount', 'email')

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
class MessageForm(forms.ModelForm):
     class Meta:
          model = Message
          fields = '__all__'
class ProfileForm(UserChangeForm):
     class Meta:
          model = User
          fields = ['username', 'email', 'first_name', 'last_name']
          exclude = ['password']
class DpForm(forms.ModelForm):
     class Meta:
          model = Dp
          fields ='__all__'
class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = '__all__'
        
class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = '__all__'
        
class SectionForm(forms.ModelForm):

    class Meta:
        model = Section
        fields = '__all__'

class ContentForm(forms.ModelForm):

    class Meta:
        model = CourseContent
        fields = '__all__'
class CourseMessageForm(forms.ModelForm):
     class Meta:
          model = CourseMessage
          fields = '__all__'
class AnnouncementForm(forms.ModelForm):
     class Meta:
          model = CourseAnnoucement
          fields = '__all__'

ContentFormSet = inlineformset_factory(
    Section, CourseContent, form=ContentForm,
    extra=1, can_delete=True,
    can_delete_extra=True
)
SectionFormSet = inlineformset_factory(
    Course, Section, form=SectionForm,
    extra=3, can_delete=True,
    can_delete_extra=True
)
class PasswordChangeForm(PasswordChangeForm):
     old_password = forms.CharField()
     new_password1 = forms.CharField()
     new_password2 = forms.CharField()

class PasswordResetForm(PasswordResetForm):
     email = forms.EmailField()

class SetMyPasswordForm(SetPasswordForm):
     new_password1 = forms.CharField()
     new_password2 = forms.CharField()
