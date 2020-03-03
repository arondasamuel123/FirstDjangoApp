from django import forms
class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First_Name', max_length=30)
    email = forms.EmailField(label='Email')
    
    
    