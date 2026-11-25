# catalogo/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Bolo
from .forms import BoloForm
from django.contrib.auth.decorators import login_required


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def pagina_inicial(request):
    return render(request, 'catalogo/index.html')

def lista_bolos(request):
    bolos = Bolo.objects.all()
    query = request.GET.get('q')
    if query:
        bolos = bolos.filter(
            Q(nome__icontains=query) | Q(sabor__icontains=query)
        )

    paginator = Paginator(bolos, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,
                  'catalogo/lista_bolos.html',
                  {'page_obj': page_obj})

@login_required()
def novo_bolo(request):
    if request.method == 'POST':
        form = BoloForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('catalogo:lista_bolos')
    else:
        form = BoloForm()

    return render(request,
                   'catalogo/bolo_form.html',
                   {'form' : form})


def detalhe_bolo(request, pk):
    # 1. Os Detalhes do Bolo
    bolo = get_object_or_404(Bolo, pk=pk)
    return render(request, 'catalogo/detalhe_bolo.html', {'bolo': bolo})

@login_required()
def editar_bolo(request, pk):
    # 2. Atualização do Estoque
    bolo = get_object_or_404(Bolo, pk=pk)

    if request.method == 'POST':
        form = BoloForm(request.POST, request.FILES, instance=bolo)
        if form.is_valid():
            form.save()
            return redirect('catalogo:detalhe_bolo', pk=bolo.pk)
    else:
        form = BoloForm(instance=bolo)

    return render(request, 'catalogo/bolo_form.html', {'form': form})

@login_required()
def apagar_bolo(request, pk):
    # 3. Fim de Linha (Excluir)
    bolo = get_object_or_404(Bolo, pk=pk)

    if request.method == 'POST':
        bolo.delete()
        return redirect('catalogo:lista_bolos')

    return render(request, 'catalogo/bolo_confirmar_exclusao.html', {'bolo': bolo})