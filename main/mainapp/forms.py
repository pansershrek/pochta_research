from django import forms


class UploadForm(forms.Form):
    file = forms.FileField(label="Json с данными об отправлении")
