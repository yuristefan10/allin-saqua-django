from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from django.utils.html import format_html
from .models import (Usuario, Estabelecimento, Quarto, ImagemQuarto,
                     Comentario, PontoTuristico, FotoTour360,
                     AvaliacaoAcessibilidade, Reserva, Evento,
                     EdicaoEstabelecimento, SolicitacaoParceria)


def status_colorido(status, label):
    cores = {'pendente': '#f0ad4e', 'aprovado': '#5cb85c', 'rejeitado': '#d9534f'}
    return format_html(
        '<span style="background:{};color:#fff;padding:3px 10px;border-radius:10px;'
        'font-size:.78rem;font-weight:600">{}</span>',
        cores.get(status, '#777'), label
    )

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
    list_display  = ['nome', 'categoria', 'status_badge', 'proprietario', 'nivel_acessibilidade', 'destaque', 'ordem_destaque']
    list_filter   = ['status', 'categoria', 'destaque', 'nivel_acessibilidade']
    list_editable = ['destaque', 'ordem_destaque']
    search_fields = ['nome', 'endereco']
    actions       = ['aprovar_estabelecimento', 'rejeitar_estabelecimento']
    fieldsets = (
        (None, {'fields': ('nome', 'descricao', 'endereco', 'telefone', 'categoria', 'imagem', 'destaque', 'ordem_destaque')}),
        ('Parceria', {'fields': ('proprietario', 'status')}),
        ACESSIBILIDADE_FIELDSET,
    )
    inlines = [QuartoInline]

    @admin.display(description='Status', ordering='status')
    def status_badge(self, obj):
        return status_colorido(obj.status, obj.get_status_display())

    @admin.action(description='Aprovar e publicar (ativa o parceiro)')
    def aprovar_estabelecimento(self, request, qs):
        for estab in qs:
            estab.status = 'aprovado'
            estab.save()
            if estab.proprietario and not estab.proprietario.is_active:
                estab.proprietario.is_active = True
                estab.proprietario.save()
        self.message_user(request, f'{qs.count()} estabelecimento(s) aprovado(s) e parceiro(s) ativado(s).')

    @admin.action(description='Rejeitar estabelecimento')
    def rejeitar_estabelecimento(self, request, qs):
        qs.update(status='rejeitado')
        self.message_user(request, f'{qs.count()} estabelecimento(s) rejeitado(s).')


@admin.register(SolicitacaoParceria)
class SolicitacaoParceriaAdmin(EstabelecimentoAdmin):
    """Menu dedicado que lista apenas as solicitações de parceria pendentes."""
    list_display  = ['nome', 'categoria', 'status_badge', 'proprietario', 'contato_parceiro', 'criado_em']
    list_filter   = ['status', 'categoria']
    list_editable = []

    def get_queryset(self, request):
        # mostra apenas as solicitações pendentes (com proprietário)
        return super().get_queryset(request).filter(
            proprietario__isnull=False, status='pendente').order_by('-criado_em')

    @admin.display(description='Contato do parceiro')
    def contato_parceiro(self, obj):
        if obj.proprietario:
            p = obj.proprietario
            return format_html('{}<br><small>{}</small>', p.get_full_name() or p.username, p.email)
        return '—'


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


@admin.register(EdicaoEstabelecimento)
class EdicaoEstabelecimentoAdmin(admin.ModelAdmin):
    list_display   = ['estabelecimento', 'solicitante', 'status', 'qtd_alteracoes', 'criado_em']
    list_filter    = ['status', 'criado_em']
    search_fields  = ['estabelecimento__nome', 'solicitante__username']
    readonly_fields = ['estabelecimento', 'solicitante', 'relatorio_alteracoes',
                       'preview_imagem_proposta', 'criado_em', 'revisado_em']
    actions        = ['aprovar_edicoes', 'rejeitar_edicoes']
    fields = ['estabelecimento', 'solicitante', 'status', 'relatorio_alteracoes',
              'preview_imagem_proposta', 'observacao_admin', 'criado_em', 'revisado_em']

    @admin.display(description='Alterações')
    def qtd_alteracoes(self, obj):
        n = len(obj.alteracoes or {})
        if obj.imagem_proposta:
            n += 1
        return f'{n} campo(s)'

    @admin.display(description='Relatório de alterações propostas')
    def relatorio_alteracoes(self, obj):
        if not obj.alteracoes:
            return 'Nenhuma alteração de texto (verifique a imagem abaixo).'
        linhas = [
            '<table style="border-collapse:collapse;width:100%;max-width:700px">',
            '<tr style="background:#417690;color:#fff">'
            '<th style="padding:8px;text-align:left">Campo</th>'
            '<th style="padding:8px;text-align:left">Valor atual</th>'
            '<th style="padding:8px;text-align:left">Novo valor</th></tr>',
        ]
        for campo, v in obj.alteracoes.items():
            rotulo = v.get('rotulo', campo)
            de = v.get('de', '')
            para = v.get('para', '')
            de = '—' if de in ('', None) else de
            para = '—' if para in ('', None) else para
            linhas.append(
                f'<tr style="border-bottom:1px solid #ddd">'
                f'<td style="padding:8px;font-weight:600">{rotulo}</td>'
                f'<td style="padding:8px;color:#b00">{de}</td>'
                f'<td style="padding:8px;color:#080">{para}</td></tr>'
            )
        linhas.append('</table>')
        return format_html(''.join(linhas))

    @admin.display(description='Nova imagem proposta')
    def preview_imagem_proposta(self, obj):
        if obj.imagem_proposta:
            return format_html('<img src="{}" style="max-height:180px;border-radius:8px">', obj.imagem_proposta.url)
        return 'Sem alteração de imagem.'

    @admin.action(description='Aprovar e aplicar alterações selecionadas')
    def aprovar_edicoes(self, request, qs):
        aplicadas = 0
        for edicao in qs.filter(status='pendente'):
            edicao.aplicar()
            edicao.status = 'aprovado'
            edicao.revisado_em = timezone.now()
            edicao.save()
            aplicadas += 1
        self.message_user(request, f'{aplicadas} edição(ões) aprovada(s) e aplicada(s) ao site.')

    @admin.action(description='Rejeitar alterações selecionadas')
    def rejeitar_edicoes(self, request, qs):
        n = qs.filter(status='pendente').update(status='rejeitado', revisado_em=timezone.now())
        self.message_user(request, f'{n} edição(ões) rejeitada(s).')


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'usuario', 'quarto', 'data_checkin', 'data_checkout', 'status']
    list_filter   = ['status']
    list_editable = ['status']


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display  = ['titulo', 'data_evento', 'local', 'tem_imagem']
    list_filter   = ['data_evento']
    search_fields = ['titulo', 'local', 'descricao']
    date_hierarchy = 'data_evento'
    fields = ['titulo', 'data_evento', 'local', 'descricao_curta', 'descricao', 'imagem', 'link_externo']

    @admin.display(description='Imagem', boolean=True)
    def tem_imagem(self, obj):
        return bool(obj.imagem)
