from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MensagemForm
from .models import Mensagens


def index(request: HttpRequest) -> HttpResponse:

    site_primas = Mensagens.objects.order_by('-id')[:6]

    contexto = {
        'titulo_pagina': 'Site_Das_Primas',
        'descricao': 'Compartilhar recados de usuarios',
        'site_primas': site_primas,
    }

    return render(request, 'core/index.html', contexto)

@login_required
def enviar(request: HttpRequest) -> HttpResponse:

    mensagem_enviada = False

    if request.method == "POST":

        form = MensagemForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            mensagem = form.save(commit=False)
            mensagem.usuario = request.user
            mensagem.save()

            messages.success(
                request,
                "Mensagem enviada com sucesso."
            )

            mensagem_enviada = True

    else:
        form = MensagemForm()

    contexto = {
        "form": form,
        "mensagem_enviada": mensagem_enviada,
    }

    return render(
        request,
        "core/enviar.html",
        contexto,
    )
def mensagens(request: HttpRequest) -> HttpResponse:

    termo_busca = request.GET.get("q", "").strip()

    mensagens = Mensagens.objects.all().order_by("-id")

    if termo_busca:
        mensagens = mensagens.filter(
            mensagem__icontains=termo_busca
        )

    contexto = {
        "mensagens": mensagens,
        "termo_busca": termo_busca,
    }

    return render(
        request,
        "core/mensagens.html",
        contexto,
    )


def cadastro_view(request: HttpRequest) -> HttpResponse:
    contexto = {}

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        sobrenome = request.POST.get("sobrenome", "").strip()
        email = request.POST.get("email", "").strip()
        senha = request.POST.get("senha", "").strip()
        confirmar_senha = request.POST.get("confirmar_senha", "").strip()

        if senha != confirmar_senha:
            contexto["erro"] = "As senhas informadas não coincidem."
            return render(request, "core/cadastro.html", contexto)

        if User.objects.filter(username=email).exists():
            contexto["erro"] = "Já existe uma conta cadastrada com este e-mail."
            return render(request, "core/cadastro.html", contexto)

        User.objects.create_user(
            username=email,
            email=email,
            password=senha,
            first_name=nome,
            last_name=sobrenome,
        )

        messages.success(request=request, message="Cadastro realizado com sucesso.")
        return redirect("core:login")  

    return render(request, "core/cadastro.html", contexto)



def login_view(request: HttpRequest) -> HttpResponse:
    contexto = {}

    next_url = request.GET.get("next", "")

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        senha = request.POST.get("senha", "")

        usuario = authenticate(request=request, username=email, password=senha)

        if usuario is not None:
            login(request=request, user=usuario)

            messages.success(request=request, message="Login realizado com sucesso.") 

            if next_url:
                return redirect(next_url)

            return redirect("core:index")
        else:
            contexto["erro"] = "E-mail ou senha inválidos."

    return render(request, "core/login.html", contexto)


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request=request)

    messages.info(request=request, message="Você saiu da sua conta.")

    return redirect("core:index")

def detalhes_mensagem(request, id):
    mensagem = Mensagens.objects.get(id=id)

    print("ID DA MENSAGEM:", mensagem.id)

    return render(
        request,
        "core/detalhes_mensagem.html",
        {"mensagem": mensagem}
    )


@login_required
def editar_mensagem(request, id):
    mensagem = get_object_or_404(
        Mensagens,
        id=id,
        usuario=request.user
    )

    if request.method == "POST":
        form = MensagemForm(
            request.POST,
            request.FILES,
            instance=mensagem,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Mensagem atualizada com sucesso."
            )

            return redirect(
                "core:detalhes_mensagem",
                id=mensagem.id
            )

    else:
        form = MensagemForm(instance=mensagem)

    return render(
        request,
        "core/editar_mensagem.html",
        {
            "mensagem": mensagem,
            "form": form,
        }
    )

@login_required
def excluir_mensagem(request, id):
    mensagem = get_object_or_404(
        Mensagens,
        id=id,
        usuario=request.user
    )

    if request.method == "POST":
        mensagem.delete()

        return redirect("core:minhas_mensagens")

    return render(
        request,
        "core/excluir_mensagem.html",
        {"mensagem": mensagem}
    )


@login_required
def minhas_mensagens(request: HttpRequest) -> HttpResponse:

    mensagens = Mensagens.objects.filter(
        usuario=request.user
    ).order_by("-id")

    contexto = {
        "mensagens": mensagens
    }

    return render(
        request=request,
        template_name="core/minhas_mensagens.html",
        context=contexto
    )

# ERROS 

def erro_400(
    request: HttpRequest,
    exception,
) -> HttpResponse:

    contexto = {
        "codigo_erro": "400",
        "titulo_erro": "Requisição inválida",
        "mensagem_erro": (
            "Não foi possível processar a solicitação "
            "enviada. Verifique os dados e tente novamente."
        ),
    }

    return render(
        request,
        "core/erro.html",
        contexto,
        status=400,
    )


def erro_403(
    request: HttpRequest,
    exception,
) -> HttpResponse:

    contexto = {
        "codigo_erro": "403",
        "titulo_erro": "Acesso não permitido",
        "mensagem_erro": (
            "Você está autenticado, mas não possui permissão para acessar este recurso."
        ),
    }

    return render(
        request,
        "core/erro.html",
        contexto,
        status=403,
    )


def erro_404(
    request: HttpRequest,
    exception,
) -> HttpResponse:

    contexto = {
        "codigo_erro": "404",
        "titulo_erro": "Página não encontrada",
        "mensagem_erro": (
            "O conteúdo que você tentou acessar "
            "não foi encontrado ou não está mais disponível."
        ),
    }

    return render(
        request,
        "core/erro.html",
        contexto,
        status=404,
    )


def erro_500(
    request: HttpRequest,
) -> HttpResponse:

    contexto = {
        "codigo_erro": "500",
        "titulo_erro": "Ocorreu um erro inesperado",
        "mensagem_erro": (
            "Não foi possível concluir a operação neste momento. "
            "Tente novamente em alguns instantes."
        ),
    }

    return render(
        request,
        "core/erro.html",
        contexto,
        status=500,
    )