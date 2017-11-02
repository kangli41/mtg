from django import forms

class SubmitjobForm(forms.Form):
    pre_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'using "," to split mulit-preference'}))
    submitter = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'job submitter'}))
    image = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ex: cg-mesh-dagw-1.6.36-9bd08e1-RELEASE-ir510.bin'}))
    mailto = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'ex: kangli@cisco.com'}))
    priority = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': '1-7'}))
    comment = forms.CharField()
    to_tims = forms.BooleanField(label='Upload To Tims',required=False)
    
    def clean_email(self):
        mailto = self.cleaned_data.get('mailto')
        if not 'cisco' in mailto:
            raise forms.ValidationError('Please use cisco mail')
        return mailto