from django.db import migrations


PONTOS = [
    {
        'titulo': 'Praia de Itaúna',
        'descricao': 'A capital nacional do surf. Ondas de até 3 metros e cerca de 2 km de extensão que recebem etapas da WSL todos os anos.',
        'sobre': (
            'A Praia de Itaúna é o cartão-postal de Saquarema e um dos points de surf mais '
            'famosos do Brasil. Suas ondas fortes e consistentes, que podem chegar a 3 metros, '
            'fizeram da cidade a sede de etapas do circuito mundial da World Surf League (WSL).\n\n'
            'Além do surf, a faixa de areia extensa é ótima para caminhadas, prática de esportes '
            'e para assistir aos campeonatos. A infraestrutura ao redor conta com quiosques, '
            'restaurantes e estacionamento.'
        ),
        'link': 'https://www.google.com/maps/search/?api=1&query=Praia+de+Ita%C3%BAna+Saquarema+RJ',
    },
    {
        'titulo': 'Praia da Vila',
        'descricao': 'Praia central de Saquarema, point de surfistas e ideal para caminhadas à beira-mar, com a Igreja de Nazareth ao fundo.',
        'sobre': (
            'A Praia da Vila fica no coração de Saquarema, logo abaixo da histórica Igreja de '
            'Nossa Senhora de Nazareth. É muito frequentada por surfistas pelas ondas consistentes '
            'e por moradores e turistas que aproveitam a orla para caminhar e relaxar.\n\n'
            'A localização central facilita o acesso a bares, restaurantes e ao comércio local, '
            'tornando a praia um dos pontos mais movimentados da cidade.'
        ),
        'link': 'https://www.google.com/maps/search/?api=1&query=Praia+da+Vila+Saquarema+RJ',
    },
    {
        'titulo': 'Lagoa de Saquarema',
        'descricao': "Espelho d'água de cerca de 17 km, perfeito para stand-up paddle, caiaque e pesca, com pôr do sol espetacular.",
        'sobre': (
            'A Lagoa de Saquarema tem aproximadamente 17 km de extensão e águas calmas, ideais '
            'para a prática de esportes aquáticos como stand-up paddle, caiaque e vela. Também é '
            'um local tradicional de pesca artesanal.\n\n'
            'O entorno da lagoa oferece vistas deslumbrantes, especialmente ao entardecer, quando '
            'o pôr do sol se reflete na água. É um dos cenários mais fotografados da cidade.'
        ),
        'link': 'https://www.google.com/maps/search/?api=1&query=Lagoa+de+Saquarema+RJ',
    },
    {
        'titulo': 'Mirante do Morro da Cruz',
        'descricao': 'No alto do Morro do Cruzeiro, uma cruz de 15 metros e vista panorâmica da cidade, das praias e da Lagoa de Saquarema.',
        'sobre': (
            'O Mirante do Morro da Cruz, localizado no Morro do Cruzeiro, é um dos pontos turísticos '
            'mais visitados de Saquarema. No topo está uma cruz metálica de 15 metros, erguida em '
            'homenagem à fé local.\n\n'
            'De lá se tem uma vista panorâmica privilegiada da cidade, das praias e da Lagoa de '
            'Saquarema. É o lugar perfeito para fotos e para apreciar o pôr do sol.'
        ),
        'link': 'https://www.google.com/maps/search/?api=1&query=Mirante+Morro+da+Cruz+Saquarema+RJ',
    },
    {
        'titulo': 'Sambaqui da Beirada',
        'descricao': 'Sítio arqueológico com cerca de 4.500 anos, registro dos antigos povos que habitaram o litoral fluminense.',
        'sobre': (
            'O Sambaqui da Beirada é um importante sítio arqueológico com cerca de 4.500 anos. '
            'Os sambaquis são montes formados por conchas, ossos e vestígios deixados pelos povos '
            'que habitaram o litoral em tempos pré-históricos.\n\n'
            'O local é um testemunho da ocupação humana antiga na região e tem grande valor '
            'histórico e científico para o estudo da pré-história brasileira.'
        ),
        'link': 'https://www.google.com/maps/search/?api=1&query=Sambaqui+da+Beirada+Saquarema+RJ',
    },
    {
        'titulo': 'Praia de Jaconé',
        'descricao': 'Praia tranquila e quase deserta na divisa com Maricá, com piscinas naturais entre as rochas na maré baixa.',
        'sobre': (
            'A Praia de Jaconé fica na divisa de Saquarema com Maricá e é conhecida por ser mais '
            'tranquila e preservada, ideal para quem busca sossego longe da agitação.\n\n'
            'Na maré baixa, formam-se piscinas naturais entre as rochas, perfeitas para banho. '
            'A região também é procurada por pescadores e por quem aprecia paisagens rústicas.'
        ),
        'link': 'https://www.google.com/maps/search/?api=1&query=Praia+de+Jacon%C3%A9+Saquarema+RJ',
    },
    {
        'titulo': 'Rampa do Voo Livre',
        'descricao': 'Ponto de salto de parapente e asa-delta no alto do morro, com vista aérea da orla e da Lagoa de Saquarema.',
        'sobre': (
            'A Rampa do Voo Livre é o ponto de partida para saltos de parapente e asa-delta em '
            'Saquarema. Localizada no alto do morro, oferece aos praticantes e visitantes uma vista '
            'aérea espetacular da orla e da lagoa.\n\n'
            'É um atrativo procurado por aventureiros e por quem deseja contemplar a paisagem de '
            'um ângulo único da cidade.'
        ),
        'link': 'https://www.google.com/maps/search/?api=1&query=Rampa+Voo+Livre+Saquarema+RJ',
    },
    {
        'titulo': 'Gruta de Nossa Senhora de Lourdes',
        'descricao': 'Gruta religiosa cercada por mata, ponto de devoção e visitação tranquila em meio à natureza saquaremense.',
        'sobre': (
            'A Gruta de Nossa Senhora de Lourdes é um espaço de fé e tranquilidade, cercado pela '
            'vegetação local. É um ponto de devoção visitado por fiéis e por turistas que apreciam '
            'o contato com a natureza.\n\n'
            'O ambiente sereno convida à reflexão e às orações, sendo mais um dos atrativos '
            'religiosos que marcam a cultura de Saquarema.'
        ),
        'link': 'https://www.google.com/maps/search/?api=1&query=Gruta+Nossa+Senhora+de+Lourdes+Saquarema+RJ',
    },
    {
        'titulo': 'Reserva Ecológica de Jacarepiá',
        'descricao': 'Área de restinga preservada, com trilhas, fauna e flora nativas da Mata Atlântica litorânea.',
        'sobre': (
            'A Reserva Ecológica de Jacarepiá protege uma área de restinga, ecossistema típico do '
            'litoral fluminense. O local abriga trilhas e uma rica biodiversidade de fauna e flora '
            'nativas da Mata Atlântica.\n\n'
            'É um destino ideal para os amantes do ecoturismo e da observação da natureza, '
            'oferecendo contato direto com a paisagem natural preservada da região.'
        ),
        'link': 'https://www.google.com/maps/search/?api=1&query=Reserva+Ecol%C3%B3gica+de+Jacarepi%C3%A1+Saquarema+RJ',
    },
    {
        'titulo': 'Praia de Barra Nova',
        'descricao': 'Faixa de areia extensa e menos movimentada, indicada para quem busca sossego e contato com a natureza.',
        'sobre': (
            'A Praia de Barra Nova oferece uma faixa de areia extensa e geralmente menos '
            'movimentada que as praias centrais. É uma boa opção para quem busca tranquilidade '
            'e um ambiente mais natural.\n\n'
            'Suas águas e paisagem agradam famílias e visitantes que querem descansar longe das '
            'multidões, aproveitando o clima litorâneo de Saquarema.'
        ),
        'link': 'https://www.google.com/maps/search/?api=1&query=Praia+de+Barra+Nova+Saquarema+RJ',
    },
]


def criar_pontos(apps, schema_editor):
    PontoTuristico = apps.get_model('portal', 'PontoTuristico')
    for dados in PONTOS:
        PontoTuristico.objects.get_or_create(
            titulo=dados['titulo'],
            defaults={
                'descricao': dados['descricao'],
                'sobre': dados['sobre'],
                'link': dados['link'],
            },
        )


def remover_pontos(apps, schema_editor):
    PontoTuristico = apps.get_model('portal', 'PontoTuristico')
    titulos = [d['titulo'] for d in PONTOS]
    PontoTuristico.objects.filter(titulo__in=titulos).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_alter_comentario_comentario_and_more'),
    ]

    operations = [
        migrations.RunPython(criar_pontos, remover_pontos),
    ]
