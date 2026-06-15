"""
Baixa imagens de licença livre (Wikimedia Commons) e associa aos pontos
turísticos que ainda não têm imagem. Idempotente: só preenche o que está vazio.

Uso:  python manage.py baixar_imagens_pontos
"""
import os
import urllib.request

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from portal.models import PontoTuristico


# titulo do ponto -> (url da imagem, crédito/licença)
IMAGENS = {
    'Praia de Itaúna': (
        'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Ita%C3%BAna_Beach.jpg/1280px-Ita%C3%BAna_Beach.jpg',
        'Foto: Wikimedia Commons (CC BY-SA 3.0)',
    ),
    'Lagoa de Saquarema': (
        'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Lagoa_de_Saquarema_-_panoramio.jpg/1280px-Lagoa_de_Saquarema_-_panoramio.jpg',
        'Foto: Wikimedia Commons (CC BY-SA 3.0)',
    ),
    'Praia da Vila': (
        'https://upload.wikimedia.org/wikipedia/commons/4/48/Barcos_na_Praia_de_Saquarema.jpg',
        'Foto: Wikimedia Commons (CC BY-SA 4.0)',
    ),
    'Praia de Jaconé': (
        'https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Bolhas_sobe_a_areia.jpg/1280px-Bolhas_sobe_a_areia.jpg',
        'Foto: Wikimedia Commons (CC BY-SA 4.0)',
    ),
    'Praia de Barra Nova': (
        'https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Noite_-_Praia_do_Boqueir%C3%A3o_-_Saquarema.jpg/1280px-Noite_-_Praia_do_Boqueir%C3%A3o_-_Saquarema.jpg',
        'Foto: Wikimedia Commons (CC BY-SA 3.0)',
    ),
    'Mirante do Morro da Cruz': (
        'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Oceano_Dourado.jpg/1280px-Oceano_Dourado.jpg',
        'Foto: Wikimedia Commons (CC BY-SA 4.0)',
    ),
}


class Command(BaseCommand):
    help = 'Baixa imagens livres do Wikimedia Commons para os pontos turísticos sem imagem.'

    def handle(self, *args, **options):
        for titulo, (url, credito) in IMAGENS.items():
            try:
                ponto = PontoTuristico.objects.get(titulo=titulo)
            except PontoTuristico.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'– Ponto não encontrado: {titulo}'))
                continue

            if ponto.imagem:
                self.stdout.write(f'• Já tem imagem, pulando: {titulo}')
                continue

            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'AllInSaqua/1.0 (turismo)'})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    dados = resp.read()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Erro ao baixar {titulo}: {e}'))
                continue

            nome_arquivo = os.path.basename(urllib.request.url2pathname(url.split('/')[-1]))
            ponto.imagem.save(nome_arquivo, ContentFile(dados), save=False)
            # adiciona o crédito ao final do texto, se ainda não estiver lá
            if credito not in (ponto.sobre or ''):
                ponto.sobre = (ponto.sobre or '').rstrip() + f'\n\n_{credito}_'
            ponto.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Imagem adicionada: {titulo}'))

        self.stdout.write(self.style.SUCCESS('Concluído.'))
