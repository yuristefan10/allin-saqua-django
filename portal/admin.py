from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Estabelecimento, Quarto, ImagemQuarto, Comentario, PontoTuristico, Reserva, Evento


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Dados extras', {'fields': ('cpf', 'telefone', 'tipo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dados extras', {'fields': ('cpf', 'telefone', 'tipo')}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'tipo', 'is_active']
    list_filter = ['tipo', 'is_active']


class QuartoInline(admin.TabularInline):
    model = Quarto
    extra = 0


class ImagemQuartoInline(admin.TabularInline):
    model = ImagemQuarto
    extra = 1


@admin.register(Estabelecimento)
class EstabelecimentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'destaque', 'ordem_destaque', 'criado_em']
    list_filter = ['categoria', 'destaque']
    list_editable = ['destaque', 'ordem_destaque']
    search_fields = ['nome', 'endereco']
    inlines = [QuartoInline]


@admin.register(Quarto)
class QuartoAdmin(admin.ModelAdmin):
    list_display = ['nome_quarto', 'estabelecimento', 'capacidade', 'preco_diaria']
    list_filter = ['estabelecimento']
    inlines = [ImagemQuartoInline]


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['estabelecimento', 'usuario', 'nota', 'status', 'data_comentario']
    list_filter = ['status', 'nota']
    list_editable = ['status']
    actions = ['aprovar', 'reprovar']

    @admin.action(description='Aprovar comentários selecionados')
    def aprovar(self, request, queryset):
        queryset.update(status='Aprovado')

    @admin.action(description='Reprovar comentários selecionados')
    def reprovar(self, request, queryset):
        queryset.update(status='Reprovado')


@admin.register(PontoTuristico)
class PontoTuristicoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'criado_em']
    search_fields = ['titulo']


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'quarto', 'data_checkin', 'data_checkout', 'status', 'data_reserva']
    list_filter = ['status']
    list_editable = ['status']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'usuario__email']


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'data_evento', 'criado_em']
