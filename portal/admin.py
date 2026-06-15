from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import (Usuario, Estabelecimento, Quarto, ImagemQuarto,
                     Comentario, PontoTuristico, FotoTour360,
                     AvaliacaoAcessibilidade, Reserva, Evento)

ACESSIBILIDADE_FIELDSET = ('Acessibilidade', {
    'fields': (
        'nivel_acessibilidade',
        ('ac_rampa', 'ac_elevador', 'ac_banheiro_adaptado', 'ac_estacionamento'),
        ('ac_piso_tatil', 'ac_libras', 'ac_braile', 'ac_audio_guia'),
        'obs_acessibilidade',
    ),
    'classes': ('collapse',),
})


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Dados extras', {'fields': ('cpf', 'telefone', 'tipo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dados extras', {'fields': ('cpf', 'telefone', 'tipo')}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'tipo', 'is_active']
    list_filter  = ['tipo', 'is_active']


class QuartoInline(admin.TabularInline):
    model = Quarto
    extra = 0


@admin.register(Estabelecimento)
class EstabelecimentoAdmin(admin.ModelAdmin):
    list_display  = ['nome', 'categoria', 'nivel_acessibilidade', 'destaque', 'ordem_destaque']
    list_filter   = ['categoria', 'destaque', 'nivel_acessibilidade']
    list_editable = ['destaque', 'ordem_destaque']
    search_fields = ['nome', 'endereco']
    fieldsets = (
        (None, {'fields': ('nome', 'descricao', 'endereco', 'telefone', 'categoria', 'imagem', 'destaque', 'ordem_destaque')}),
        ACESSIBILIDADE_FIELDSET,
    )
    inlines = [QuartoInline]


@admin.register(Quarto)
class QuartoAdmin(admin.ModelAdmin):
    list_display = ['nome_quarto', 'estabelecimento', 'capacidade', 'preco_diaria']
    inlines      = [type('ImagemQuartoInline', (admin.TabularInline,), {'model': ImagemQuarto, 'extra': 1})]


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display  = ['estabelecimento', 'usuario', 'nota', 'status', 'data_comentario']
    list_filter   = ['status', 'nota']
    list_editable = ['status']
    actions       = ['aprovar', 'reprovar']

    @admin.action(description='Aprovar selecionados')
    def aprovar(self, request, qs): qs.update(status='Aprovado')

    @admin.action(description='Reprovar selecionados')
    def reprovar(self, request, qs): qs.update(status='Reprovado')


class FotoTour360Inline(admin.TabularInline):
    model  = FotoTour360
    extra  = 1
    fields = ['titulo', 'foto', 'ordem', 'descricao']


class PontoTuristicoForm(forms.ModelForm):
    class Meta:
        model = PontoTuristico
        fields = '__all__'
        help_texts = {
            'descricao': 'Resumo curto (máx. 190 caracteres) exibido nos cards e nos resultados de busca.',
            'sobre': 'Texto completo exibido na página de detalhe. Pode ter vários parágrafos.',
            'link': 'Link externo, ex.: localização no Google Maps.',
            'imagem': 'Imagem de capa em paisagem. Recomendado 1200×400 px (.jpg, .png, .webp).',
        }
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 2}),
        }


@admin.register(PontoTuristico)
class PontoTuristicoAdmin(admin.ModelAdmin):
    form = PontoTuristicoForm
    list_display  = ['titulo', 'nivel_acessibilidade', 'tour_tipo', 'tem_imagem', 'qtd_fotos_360', 'criado_em']
    list_filter   = ['nivel_acessibilidade', 'tour_tipo']
    search_fields = ['titulo', 'descricao', 'sobre']
    date_hierarchy = 'criado_em'
    list_per_page = 25
    readonly_fields = ['preview_imagem']
    fieldsets = (
        (None, {'fields': ('titulo', 'descricao', 'sobre', 'link')}),
        ('Imagem de capa', {'fields': ('imagem', 'preview_imagem')}),
        ('Tour 360°', {
            'fields': ('tour_tipo', 'tour_streetview_url'),
            'description': '📱 Selecione o tipo. Para Foto 360°, adicione as cenas na seção abaixo. Para Street View, cole a URL de embed do Google Maps.',
        }),
        ACESSIBILIDADE_FIELDSET,
    )
    inlines = [FotoTour360Inline]

    @admin.display(description='Imagem', boolean=True)
    def tem_imagem(self, obj):
        return bool(obj.imagem)

    @admin.display(description='Fotos 360°')
    def qtd_fotos_360(self, obj):
        return obj.fotos_360.count()

    @admin.display(description='Pré-visualização')
    def preview_imagem(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" style="max-height:180px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,.2)">',
                obj.imagem.url
            )
        return 'Nenhuma imagem enviada ainda.'


@admin.register(AvaliacaoAcessibilidade)
class AvaliacaoAcessibilidadeAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo_local', 'ponto', 'estabelecimento', 'nota', 'data']
    list_filter  = ['tipo_local', 'nota']


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'usuario', 'quarto', 'data_checkin', 'data_checkout', 'status']
    list_filter   = ['status']
    list_editable = ['status']


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'data_evento', 'criado_em']
