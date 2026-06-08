from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator

from .models import Estabelecimento, PontoTuristico, Quarto, Reserva, Evento, Comentario
from .forms import CadastroForm, LoginForm, ReservaForm, ComentarioForm


# ── Páginas públicas ──────────────────────────────────────────────────────────

def index(request):
    destaques = Estabelecimento.objects.filter(destaque=True).order_by('ordem_destaque', 'nome')[:5]
    eventos = Evento.objects.order_by('-data_evento')[:3]
    return render(request, 'portal/index.html', {'destaques': destaques, 'eventos': eventos})


def sobre(request):
    return render(request, 'portal/sobre.html')


def contato(request):
    return render(request, 'portal/contato.html')


def servicos(request):
    estabelecimentos = Estabelecimento.objects.filter(categoria='Serviço')
    return render(request, 'portal/servicos.html', {'estabelecimentos': estabelecimentos})


# ── Pontos turísticos ─────────────────────────────────────────────────────────

def turismo(request):
    pontos = PontoTuristico.objects.order_by('-criado_em')
    return render(request, 'portal/turismo.html', {'pontos': pontos})


def detalhe_ponto(request, pk):
    ponto = get_object_or_404(PontoTuristico, pk=pk)
    return render(request, 'portal/detalhe_ponto.html', {'ponto': ponto})


# ── Estabelecimentos ──────────────────────────────────────────────────────────

def lojas(request):
    categoria = request.GET.get('categoria', '')
    estabelecimentos = Estabelecimento.objects.all()
    if categoria:
        estabelecimentos = estabelecimentos.filter(categoria=categoria)
    categorias = Estabelecimento.CATEGORIA_CHOICES
    return render(request, 'portal/lojas.html', {
        'estabelecimentos': estabelecimentos,
        'categorias': categorias,
        'categoria_atual': categoria,
    })


def detalhe_estabelecimento(request, pk):
    estab = get_object_or_404(Estabelecimento, pk=pk)
    comentarios = estab.comentarios.filter(status='Aprovado').order_by('-data_comentario')
    form = ComentarioForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Faça login para comentar.')
            return redirect('login')
        form = ComentarioForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.estabelecimento = estab
            c.usuario = request.user
            c.save()
            messages.success(request, 'Comentário enviado para aprovação.')
            return redirect('detalhe_estabelecimento', pk=pk)

    return render(request, 'portal/detalhe_estabelecimento.html', {
        'estab': estab,
        'comentarios': comentarios,
        'form': form,
    })


# ── Quartos e reservas ────────────────────────────────────────────────────────

def ver_quartos(request, estab_pk):
    estab = get_object_or_404(Estabelecimento, pk=estab_pk)
    quartos = estab.quartos.prefetch_related('imagens')
    return render(request, 'portal/ver_quartos.html', {'estab': estab, 'quartos': quartos})


def detalhe_quarto(request, pk):
    quarto = get_object_or_404(Quarto, pk=pk)
    return render(request, 'portal/detalhe_quarto.html', {'quarto': quarto})


@login_required
def fazer_reserva(request, quarto_pk):
    quarto = get_object_or_404(Quarto, pk=quarto_pk)
    form = ReservaForm(request.POST or None)
    if form.is_valid():
        reserva = form.save(commit=False)
        reserva.quarto = quarto
        reserva.usuario = request.user
        reserva.save()
        messages.success(request, 'Reserva realizada com sucesso!')
        return redirect('reserva_sucesso', pk=reserva.pk)
    return render(request, 'portal/fazer_reserva.html', {'quarto': quarto, 'form': form})


@login_required
def reserva_sucesso(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk, usuario=request.user)
    return render(request, 'portal/reserva_sucesso.html', {'reserva': reserva})


@login_required
def consultar_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-data_reserva')
    return render(request, 'portal/consultar_reservas.html', {'reservas': reservas})


# ── Auth ──────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get('next', 'index'))
    return render(request, 'portal/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


def cadastro_view(request):
    form = CadastroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Bem-vindo, {user.first_name}!')
        return redirect('index')
    return render(request, 'portal/cadastro.html', {'form': form})


@login_required
def perfil(request):
    return render(request, 'portal/perfil.html')
