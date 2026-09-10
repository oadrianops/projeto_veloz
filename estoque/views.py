from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Ingrediente

def lista_compras(request):
    ingredientes = Ingrediente.objects.all()
    lista_final = []

    for item in ingredientes:
        quantidade_comprar = 0

        # Regra 1: Ingrediente estragou/venceu
        # Descarta a sobra e compra a meta inteira
        if item.vencido:
            quantidade_comprar = item.meta
            
        # Regra 2: Faltou antes do fim do mês
        # Compra o total que foi consumido mais uma margem de 20%[cite: 1]
        elif item.faltou_antes_do_fim:
            quantidade_comprar = float(item.consumo_real) * 1.20
            
        # Regra 3: Fluxo Padrão
        # Compra apenas a diferença para voltar à meta inicial[cite: 1]
        else:
            quantidade_comprar = float(item.meta) - float(item.estoque_atual)

        # Filtro: Ignorar itens com quantidade zero ou negativa[cite: 1]
        if quantidade_comprar > 0:
            lista_final.append({
                'nome': item.nome,
                # Formata para remover casas decimais inúteis (ex: 12.0 vira 12)
                'quantidade': round(quantidade_comprar, 2) if quantidade_comprar % 1 else int(quantidade_comprar),
                'unidade': item.unidade
            })

    return render(request, 'estoque/lista_compras.html', {'compras': lista_final})