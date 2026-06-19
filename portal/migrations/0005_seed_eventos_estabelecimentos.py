"""
Popula o calendário de eventos de 2026 (fonte: calendário oficial da
Prefeitura de Saquarema) e cria estabelecimentos de exemplo.

Idempotente: usa get_or_create por nome/título.
As datas usam o dia de início de cada evento.
"""
import datetime

from django.db import migrations


EVENTOS = [
    {
        'titulo': 'Festival de Verão',
        'descricao_curta': 'Alta temporada com grandes shows na Praia de Itaúna durante todo o mês de janeiro. Música, esporte e lazer para toda a família.',
        'data_evento': datetime.date(2026, 1, 10),
    },
    {
        'titulo': 'Carnaval de Saquarema',
        'descricao_curta': 'Folia, blocos e muita música espalhados pela cidade no feriado de Carnaval.',
        'data_evento': datetime.date(2026, 2, 13),
    },
    {
        'titulo': 'Saquarema Country Fest',
        'descricao_curta': 'O maior festival sertanejo e rodeio da região, que reúne mais de 100 mil pessoas no feriado de maio.',
        'data_evento': datetime.date(2026, 5, 1),
    },
    {
        'titulo': 'Saquá Moto Rock',
        'descricao_curta': 'Tradicional encontro de motociclistas com shows de rock, exposições e muita adrenalina.',
        'data_evento': datetime.date(2026, 5, 21),
    },
    {
        'titulo': 'Arraiá da Vila',
        'descricao_curta': 'Festa junina tradicional de Saquarema, com quadrilhas, comidas típicas e música ao vivo na Vila.',
        'data_evento': datetime.date(2026, 7, 17),
    },
    {
        'titulo': 'O Gosto de Agosto',
        'descricao_curta': 'Festival gastronômico que celebra a culinária local com pratos especiais nos restaurantes da cidade durante agosto.',
        'data_evento': datetime.date(2026, 8, 1),
    },
    {
        'titulo': 'Círio de Nazareth',
        'descricao_curta': 'A maior e mais antiga festa religiosa de Saquarema, com a procissão de Nossa Senhora de Nazareth, padroeira da cidade.',
        'data_evento': datetime.date(2026, 9, 4),
    },
    {
        'titulo': 'Saquarema Beer Fest',
        'descricao_curta': 'Festival de cervejas artesanais com food trucks, música ao vivo e produtores da região.',
        'data_evento': datetime.date(2026, 10, 9),
    },
    {
        'titulo': 'FLIS – Feira Literária de Saquarema',
        'descricao_curta': 'Encontro literário com escritores, palestras, oficinas e atividades culturais para todas as idades.',
        'data_evento': datetime.date(2026, 11, 11),
    },
    {
        'titulo': 'Natal de Luz',
        'descricao_curta': 'Saquarema se enche de luz no Natal, com decoração especial, presépios e atrações para toda a família durante dezembro.',
        'data_evento': datetime.date(2026, 12, 1),
    },
    {
        'titulo': 'Réveillon de Saquarema',
        'descricao_curta': 'Virada do ano à beira-mar, com queima de fogos e shows para celebrar a chegada de 2027.',
        'data_evento': datetime.date(2026, 12, 29),
    },
]


ESTABELECIMENTOS = [
    {
        'nome': 'Pousada Mar Azul',
        'descricao': 'Estabelecimento de exemplo — edite ou remova no painel admin. Pousada aconchegante a poucos passos da praia.',
        'categoria': 'Pousada',
    },
    {
        'nome': 'Restaurante Sabor da Vila',
        'descricao': 'Estabelecimento de exemplo — edite ou remova no painel admin. Culinária regional e frutos do mar fresquinhos.',
        'categoria': 'Restaurante',
    },
    {
        'nome': 'Surf & Sol Shop',
        'descricao': 'Estabelecimento de exemplo — edite ou remova no painel admin. Artigos de surf, moda praia e acessórios.',
        'categoria': 'Loja',
    },
]


def criar(apps, schema_editor):
    Evento = apps.get_model('portal', 'Evento')
    Estabelecimento = apps.get_model('portal', 'Estabelecimento')

    for dados in EVENTOS:
        Evento.objects.get_or_create(
            titulo=dados['titulo'],
            defaults={
                'descricao_curta': dados['descricao_curta'],
                'data_evento': dados['data_evento'],
            },
        )

    for dados in ESTABELECIMENTOS:
        Estabelecimento.objects.get_or_create(
            nome=dados['nome'],
            defaults={
                'descricao': dados['descricao'],
                'categoria': dados['categoria'],
            },
        )


def remover(apps, schema_editor):
    Evento = apps.get_model('portal', 'Evento')
    Estabelecimento = apps.get_model('portal', 'Estabelecimento')
    Evento.objects.filter(titulo__in=[e['titulo'] for e in EVENTOS]).delete()
    Estabelecimento.objects.filter(nome__in=[e['nome'] for e in ESTABELECIMENTOS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_seed_pontos_turisticos'),
    ]

    operations = [
        migrations.RunPython(criar, remover),
    ]
