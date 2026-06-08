from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Reserva, Comentario


class CadastroForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label='Nome')
    last_name = forms.CharField(max_length=50, label='Sobrenome')
    email = forms.EmailField(label='E-mail')
    cpf = forms.CharField(max_length=11, label='CPF (somente números)')
    telefone = forms.CharField(max_length=20, required=False, label='Telefone')

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'cpf', 'telefone', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.cpf = self.cleaned_data['cpf']
        user.telefone = self.cleaned_data.get('telefone', '')
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuário ou E-mail')


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['data_checkin', 'data_checkout', 'numero_hospedes']
        widgets = {
            'data_checkin': forms.DateInput(attrs={'type': 'date'}),
            'data_checkout': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned = super().clean()
        checkin = cleaned.get('data_checkin')
        checkout = cleaned.get('data_checkout')
        if checkin and checkout and checkout <= checkin:
            raise forms.ValidationError('A data de checkout deve ser posterior ao checkin.')
        return cleaned


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['comentario', 'nota']
        widgets = {
            'nota': forms.Select(choices=[(i, f'{i} estrela{"s" if i > 1 else ""}') for i in range(1, 6)]),
            'comentario': forms.Textarea(attrs={'rows': 4}),
        }
