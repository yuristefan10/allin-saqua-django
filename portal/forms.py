from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from .models import Usuario, Reserva, Comentario, Estabelecimento, CAMPOS_EDITAVEIS_ESTAB


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


class SolicitacaoParceriaForm(forms.Form):
    # Dados do responsável / login
    first_name = forms.CharField(max_length=50, label='Seu nome')
    last_name  = forms.CharField(max_length=50, label='Seu sobrenome')
    email      = forms.EmailField(label='E-mail')
    cpf        = forms.CharField(max_length=11, label='CPF (somente números)')
    telefone   = forms.CharField(max_length=20, required=False, label='Telefone para contato')
    username   = forms.CharField(max_length=150, label='Nome de usuário (para login)')
    password1  = forms.CharField(widget=forms.PasswordInput, label='Senha')
    password2  = forms.CharField(widget=forms.PasswordInput, label='Confirme a senha')
    # Dados do estabelecimento
    nome_estabelecimento = forms.CharField(max_length=100, label='Nome do estabelecimento')
    categoria  = forms.ChoiceField(choices=Estabelecimento.CATEGORIA_CHOICES, label='Categoria')
    descricao  = forms.CharField(max_length=255, widget=forms.Textarea(attrs={'rows': 2}), label='Descrição curta')
    endereco   = forms.CharField(max_length=255, required=False, label='Endereço')
    telefone_estabelecimento = forms.CharField(max_length=20, required=False, label='Telefone do estabelecimento')

    def clean_username(self):
        u = self.cleaned_data['username']
        if Usuario.objects.filter(username=u).exists():
            raise forms.ValidationError('Este nome de usuário já está em uso.')
        return u

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if Usuario.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError('Já existe uma conta com este CPF.')
        return cpf

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get('password1'), cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'As senhas não conferem.')
        elif p1:
            try:
                validate_password(p1)
            except forms.ValidationError as e:
                self.add_error('password1', e)
        return cleaned

    def save(self):
        d = self.cleaned_data
        user = Usuario(
            username=d['username'], email=d['email'],
            first_name=d['first_name'], last_name=d['last_name'],
            cpf=d['cpf'], telefone=d.get('telefone', ''),
            tipo='parceiro', is_active=False,
        )
        user.set_password(d['password1'])
        user.save()
        estab = Estabelecimento.objects.create(
            nome=d['nome_estabelecimento'], descricao=d['descricao'],
            categoria=d['categoria'], endereco=d.get('endereco', ''),
            telefone=d.get('telefone_estabelecimento', ''),
            proprietario=user, status='pendente',
        )
        return user, estab


class EstabelecimentoParceiroForm(forms.ModelForm):
    """Formulário que o parceiro usa para propor alterações no seu estabelecimento."""
    class Meta:
        model = Estabelecimento
        fields = [f for f, _ in CAMPOS_EDITAVEIS_ESTAB] + ['imagem']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 2}),
            'obs_acessibilidade': forms.Textarea(attrs={'rows': 3}),
        }
