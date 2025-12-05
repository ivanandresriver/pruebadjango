from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label='Usuario')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')
    image_url = forms.URLField(required=False, label='URL imagen')

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        # Normalizar image_url: si el usuario pegó "www.example.com/img.jpg" añadimos https://
        image = cleaned.get('image_url')
        if image:
            if not (image.startswith('http://') or image.startswith('https://')):
                cleaned['image_url'] = 'https://' + image
        return cleaned


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
