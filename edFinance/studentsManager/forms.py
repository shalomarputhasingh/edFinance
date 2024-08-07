from django import forms
from django.forms import ModelForm
from .models import Student
class UploadFileForm(forms.Form):
    file = forms.FileField()

class editStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['id_no','school', 'school_name','school_username']
