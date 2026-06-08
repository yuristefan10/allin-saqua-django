from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Usuario(AbstractUser):
    TIPO_CHOICES = [('admin', 'Admin'), ('comum', 'Comum')]
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='comum')

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def is_admin_portal(self):
        return self.tipo == 'admin'


class Estabelecimento(models.Model):
    CATEGORIA_CHOICES = [
        ('Restaurante', 'Restaurante'),
        ('Pousada', 'Pousada'),
        ('Loja', 'Loja'),
        ('Serviço', 'Serviço'),
        ('Outro', 'Outro'),
    ]
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    imagem = models.ImageField(upload_to='estabelecimentos/', blank=True, null=True)
    destaque = models.BooleanField(default=False)
    ordem_destaque = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Estabelecimento'
        verbose_name_plural = 'Estabelecimentos'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Quarto(models.Model):
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE, related_name='quartos')
    nome_quarto = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    capacidade = models.IntegerField(default=1)
    preco_diaria = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Quarto'
        verbose_name_plural = 'Quartos'

    def __str__(self):
        return f'{self.nome_quarto} — {self.estabelecimento.nome}'


class ImagemQuarto(models.Model):
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='quartos/')
    ordem = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordem']


class Comentario(models.Model):
    STATUS_CHOICES = [('Pendente', 'Pendente'), ('Aprovado', 'Aprovado'), ('Reprovado', 'Reprovado')]
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comentario = models.TextField()
    nota = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    data_comentario = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pendente')

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'

    def __str__(self):
        return f'{self.usuario.get_full_name()} — {self.estabelecimento.nome}'


class PontoTuristico(models.Model):
    titulo = models.CharField(max_length=60)
    descricao = models.CharField(max_length=190)
    sobre = models.TextField()
    link = models.URLField(max_length=250, blank=True)
    imagem = models.ImageField(upload_to='pontos/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ponto Turístico'
        verbose_name_plural = 'Pontos Turísticos'

    def __str__(self):
        return self.titulo


class Reserva(models.Model):
    STATUS_CHOICES = [('Pendente', 'Pendente'), ('Confirmada', 'Confirmada'), ('Cancelada', 'Cancelada')]
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE, related_name='reservas')
    usuario = models.ForeignKey(Usuario, on_delete=models.RESTRICT, related_name='reservas')
    data_checkin = models.DateField()
    data_checkout = models.DateField()
    numero_hospedes = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pendente')
    data_reserva = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f'Reserva #{self.pk} — {self.usuario.get_full_name()}'

    def total_noites(self):
        return (self.data_checkout - self.data_checkin).days

    def valor_total(self):
        return self.total_noites() * self.quarto.preco_diaria


class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao_curta = models.CharField(max_length=255, blank=True)
    data_evento = models.DateField(blank=True, null=True)
    imagem = models.ImageField(upload_to='eventos/', blank=True, null=True)
    link_externo = models.URLField(max_length=255, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return self.titulo
