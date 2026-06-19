"""Preenche o campo `local` dos eventos com locais conhecidos."""
from django.db import migrations


LOCAIS = {
    'Festival de Verão': 'Praia de Itaúna, Saquarema',
    'Carnaval de Saquarema': 'Centro, Saquarema',
    'Arraiá da Vila': 'Praia da Vila, Saquarema',
    'Círio de Nazareth': 'Igreja de Nossa Senhora de Nazareth, Saquarema',
    'Natal de Luz': 'Centro, Saquarema',
    'Réveillon de Saquarema': 'Praia de Itaúna, Saquarema',
}


def preencher(apps, schema_editor):
    Evento = apps.get_model('portal', 'Evento')
    for titulo, local in LOCAIS.items():
        Evento.objects.filter(titulo=titulo, local='').update(local=local)


def reverter(apps, schema_editor):
    Evento = apps.get_model('portal', 'Evento')
    Evento.objects.filter(titulo__in=LOCAIS.keys()).update(local='')


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_alter_evento_options_evento_descricao_evento_local_and_more'),
    ]

    operations = [
        migrations.RunPython(preencher, reverter),
    ]
