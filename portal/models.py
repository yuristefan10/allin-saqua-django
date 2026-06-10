from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import os

ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(f'Tipo de arquivo não permitido. Use: {", ".join(ALLOWED_IMAGE_EXTENSIONS)}')


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

    def save(self, *args, **kwargs):
        if self.tipo == 'admin':
            self.is_staff = True
        super().save(*args, **kwargs)


# ── Acessibilidade ────────────────────────────────────────────────────────────

NIVEL_ACESSIBILIDADE_CHOICES = [
    ('nao_avaliado', 'Não avaliado'),
    ('basico',       'Básico'),
    ('intermediario','Intermediário'),
    ('completo',     'Completo'),
]

class RecursosAcessibilidadeMixin(models.Model):
    """Campos de acessibilidade reutilizáveis em Estabelecimento e PontoTuristico."""
    nivel_acessibilidade = models.CharField(
        max_length=20, choices=NIVEL_ACESSIBILIDADE_CHOICES,
        default='nao_avaliado', verbose_name='Nível de Acessibilidade'
    )
    # Recursos físicos
    ac_rampa            = models.BooleanField(default=False, verbose_name='Rampa de acesso')
    ac_elevador         = models.BooleanField(default=False, verbose_name='Elevador')
    ac_banheiro_adaptado= models.BooleanField(default=False, verbose_name='Banheiro adaptado (PCD)')
    ac_estacionamento   = models.BooleanField(default=False, verbose_name='Vaga de estacionamento PCD')
    ac_piso_tatil       = models.BooleanField(default=False, verbose_name='Piso tátil')
    # Recursos sensoriais
    ac_libras           = models.BooleanField(default=False, verbose_name='Atendimento em Libras')
    ac_braile           = models.BooleanField(default=False, verbose_name='Informações em Braille')
    ac_audio_guia       = models.BooleanField(default=False, verbose_name='Audioguia')
    # Observação
    obs_acessibilidade  = models.TextField(blank=True, verbose_name='Observações de acessibilidade')

    class Meta:
        abstract = True

    def recursos_lista(self):
        """Retorna lista de recursos ativos com nome e ícone."""
        campos = [
            ('ac_rampa',             'Rampa',             '♿'),
            ('ac_elevador',          'Elevador',          '🛗'),
            ('ac_banheiro_adaptado', 'Banheiro PCD',      '🚻'),
            ('ac_estacionamento',    'Vaga PCD',          '🅿️'),
            ('ac_piso_tatil',        'Piso tátil',        '👣'),
            ('ac_libras',            'Libras',            '🤟'),
            ('ac_braile',            'Braille',           '⠿'),
            ('ac_audio_guia',        'Audioguia',         '🎧'),
        ]
        return [(icone, nome) for campo, nome, icone in campos if getattr(self, campo)]


class Estabelecimento(RecursosAcessibilidadeMixin):
    CATEGORIA_CHOICES = [
        ('Restaurante', 'Restaurante'),
        ('Pousada', 'Pousada'),
        ('Loja', 'Loja'),
        ('Serviço', 'Serviço'),
        ('Outro', 'Outro'),
    ]
    nome           = models.CharField(max_length=100)
    descricao      = models.CharField(max_length=255)
    endereco       = models.CharField(max_length=255, blank=True)
    telefone       = models.CharField(max_length=20, blank=True)
    categoria      = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    imagem         = models.ImageField(upload_to='estabelecimentos/', blank=True, null=True, validators=[validate_image_extension])
    destaque       = models.BooleanField(default=False)
    ordem_destaque = models.IntegerField(default=0)
    criado_em      = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Estabelecimento'
        verbose_name_plural = 'Estabelecimentos'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Quarto(models.Model):
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE, related_name='quartos')
    nome_quarto     = models.CharField(max_length=100)
    descricao       = models.TextField(blank=True)
    capacidade      = models.IntegerField(default=1)
    preco_diaria    = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Quarto'
        verbose_name_plural = 'Quartos'

    def __str__(self):
        return f'{self.nome_quarto} — {self.estabelecimento.nome}'


class ImagemQuarto(models.Model):
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='quartos/')
    ordem  = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordem']


class Comentario(models.Model):
    STATUS_CHOICES = [('Pendente', 'Pendente'), ('Aprovado', 'Aprovado'), ('Reprovado', 'Reprovado')]
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE, related_name='comentarios')
    usuario         = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comentario      = models.TextField(max_length=1000)
    nota            = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    data_comentario = models.DateTimeField(auto_now_add=True)
    status          = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pendente')

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'


# ── Ponto Turístico com Tour 360° e Acessibilidade ───────────────────────────

class PontoTuristico(RecursosAcessibilidadeMixin):
    titulo    = models.CharField(max_length=60)
    descricao = models.CharField(max_length=190)
    sobre     = models.TextField()
    link      = models.URLField(max_length=250, blank=True)
    imagem    = models.ImageField(upload_to='pontos/', blank=True, null=True, validators=[validate_image_extension])
    criado_em = models.DateTimeField(auto_now_add=True)

    # Tour 360°
    tour_tipo = models.CharField(
        max_length=20,
        choices=[('nenhum', 'Sem tour'), ('pannellum', 'Foto 360° (upload)'), ('streetview', 'Google Street View')],
        default='nenhum',
        verbose_name='Tipo de Tour 360°'
    )
    # Para Pannellum: foto equirretangular
    tour_foto_360 = models.ImageField(
        upload_to='tours360/', blank=True, null=True,
        verbose_name='Foto 360° (equirretangular)',
        help_text='Exporte do app "360 Photo Camera" no Android e faça upload aqui.'
    )
    # Para Google Street View: embed URL ou coordenadas
    tour_streetview_url = models.URLField(
        blank=True,
        verbose_name='URL do Google Street View',
        help_text='Ex: https://www.google.com/maps/embed?pb=...'
    )

    def clean(self):
        super().clean()
        if self.tour_streetview_url:
            if not self.tour_streetview_url.startswith('https://www.google.com/maps/'):
                raise ValidationError({'tour_streetview_url': 'A URL deve ser do Google Maps (https://www.google.com/maps/...)'})

    class Meta:
        verbose_name = 'Ponto Turístico'
        verbose_name_plural = 'Pontos Turísticos'

    def __str__(self):
        return self.titulo

    def tem_tour(self):
        return self.tour_tipo != 'nenhum'


class FotoTour360(models.Model):
    """Múltiplas cenas para o tour de um ponto turístico."""
    ponto      = models.ForeignKey(PontoTuristico, on_delete=models.CASCADE, related_name='fotos_360')
    titulo     = models.CharField(max_length=80, verbose_name='Nome da cena')
    foto       = models.ImageField(upload_to='tours360/', verbose_name='Foto equirretangular', validators=[validate_image_extension])
    ordem      = models.IntegerField(default=0)
    descricao  = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['ordem']
        verbose_name = 'Foto do Tour 360°'
        verbose_name_plural = 'Fotos do Tour 360°'

    def __str__(self):
        return f'{self.ponto.titulo} — {self.titulo}'


# ── Avaliação de Acessibilidade pelos usuários ────────────────────────────────

class AvaliacaoAcessibilidade(models.Model):
    TIPO_LOCAL = [('ponto', 'Ponto Turístico'), ('estab', 'Estabelecimento')]
    tipo_local      = models.CharField(max_length=10, choices=TIPO_LOCAL)
    ponto           = models.ForeignKey(PontoTuristico, on_delete=models.CASCADE, null=True, blank=True, related_name='avaliacoes_acessibilidade')
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE, null=True, blank=True, related_name='avaliacoes_acessibilidade')
    usuario         = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nota            = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Nota de acessibilidade')
    comentario      = models.TextField(blank=True)
    data            = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Avaliação de Acessibilidade'
        verbose_name_plural = 'Avaliações de Acessibilidade'
        unique_together = [['usuario', 'ponto'], ['usuario', 'estabelecimento']]

    def __str__(self):
        return f'{self.usuario} — nota {self.nota}'


# ── Reserva e Evento ──────────────────────────────────────────────────────────

class Reserva(models.Model):
    STATUS_CHOICES = [('Pendente', 'Pendente'), ('Confirmada', 'Confirmada'), ('Cancelada', 'Cancelada')]
    quarto          = models.ForeignKey(Quarto, on_delete=models.CASCADE, related_name='reservas')
    usuario         = models.ForeignKey(Usuario, on_delete=models.RESTRICT, related_name='reservas')
    data_checkin    = models.DateField()
    data_checkout   = models.DateField()
    numero_hospedes = models.IntegerField(default=1)
    status          = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pendente')
    data_reserva    = models.DateTimeField(auto_now_add=True)

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
    titulo         = models.CharField(max_length=100)
    descricao_curta= models.CharField(max_length=255, blank=True)
    data_evento    = models.DateField(blank=True, null=True)
    imagem         = models.ImageField(upload_to='eventos/', blank=True, null=True, validators=[validate_image_extension])
    link_externo   = models.URLField(max_length=255, blank=True)
    criado_em      = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return self.titulo
