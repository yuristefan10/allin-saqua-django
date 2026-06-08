from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    path('servicos/', views.servicos, name='servicos'),

    path('turismo/', views.turismo, name='turismo'),
    path('turismo/<int:pk>/', views.detalhe_ponto, name='detalhe_ponto'),

    path('lojas/', views.lojas, name='lojas'),
    path('lojas/<int:pk>/', views.detalhe_estabelecimento, name='detalhe_estabelecimento'),
    path('lojas/<int:estab_pk>/quartos/', views.ver_quartos, name='ver_quartos'),

    path('quartos/<int:pk>/', views.detalhe_quarto, name='detalhe_quarto'),
    path('quartos/<int:quarto_pk>/reservar/', views.fazer_reserva, name='fazer_reserva'),
    path('reservas/<int:pk>/sucesso/', views.reserva_sucesso, name='reserva_sucesso'),
    path('reservas/', views.consultar_reservas, name='consultar_reservas'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('perfil/', views.perfil, name='perfil'),
]
