from django.urls import path

from core import views

app_name = 'core'


urlpatterns = [

    path(
        '',
        views.index,
        name='index'
    ),

    path(
        'enviar/',
        views.enviar,
        name='enviar',
    ),

    path(
        'mensagens/',
        views.mensagens,
        name='mebsagens',
    ),

    path(
        'cadastro/',
        views.cadastro_view,
        name='cadastro',
    ),

    path(
        'login/',
        views.login_view,
        name='login',
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout',
    ),

    path(
        'minhas-mensagens/',
        views.minhas_mensagens,
        name='minhas_mensagens',
    ),

   
    path(
        'mensagem/<int:id>/',
        views.detalhes_mensagem,
        name='detalhes_mensagem',
    ),

    path(
        'mensagem/<int:id>/editar/',
        views.editar_mensagem,
        name='editar_mensagem',
    ),

  
    path(
        'mensagem/<int:id>/excluir/',
        views.excluir_mensagem,
        name='excluir_mensagem',
    ),
]
