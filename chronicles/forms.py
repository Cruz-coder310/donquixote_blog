from django import forms


class EmailPostForm(forms.Form):
    subject = forms.CharField(max_length=50)
    message = forms.CharField(required=False, widget=forms.Textarea)
    from_email = forms.EmailField()
    to_email = forms.EmailField()
