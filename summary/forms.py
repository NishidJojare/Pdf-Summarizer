from django import forms
from summary.models import Upload_Pdf

class Upload_Pdf_Form(forms.ModelForm):
    class Meta:
        model=Upload_Pdf
        fields = '__all__'
        
