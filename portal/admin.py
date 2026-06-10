from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
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


@admin.register(PontoTuristico)
class PontoTuristicoAdmin(admin.ModelAdmin):
    list_display  = ['titulo', 'nivel_acessibilidade', 'tour_tipo', 'criado_em']
    list_filter   = ['nivel_acessibilidade', 'tour_tipo']
    search_fields = ['titulo']
    fieldsets = (
        (None, {'fields': ('titulo', 'descricao', 'sobre', 'link', 'imagem')}),
        ('Tour 360°', {
            'fields': ('tour_tipo', 'tour_streetview_url'),
            'description': '📱 Selecione o tipo. Para Foto 360°, adicione as cenas na seção abaixo. Para Street View, cole a URL de embed do Google Maps.',
        }),
        ACESSIBILIDADE_FIELDSET,
    )
    inlines = [FotoTour360Inline]


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
