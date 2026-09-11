# Controle de Estoque — Restaurante do Seu Raimundo

Sistema de reposição de estoque feito em Django para o desafio técnico do processo seletivo.

A ideia é simples: o Seu Raimundo cadastra os ingredientes do restaurante, informa quanto tem
guardado e o que aconteceu com cada item no mês, e o sistema devolve a lista de compras pronta
para o rapaz levar à feira.

## Projeto online

A aplicação está hospedada e pode ser acessada sem instalar nada:

- Lista de compras: https://estoque.nandesk.com.br/
- Painel administrativo: https://estoque.nandesk.com.br/admin/

Está rodando em uma VPS com Coolify, usando Gunicorn e WhiteNoise para servir os arquivos
estáticos.

## As regras de negócio

Tirei as regras da própria conversa com o cliente. São três situações possíveis para cada
ingrediente, e elas se excluem — cada item cai em uma delas.

**1. O ingrediente venceu.** Ele disse que quando o troço vence joga tudo fora, não interessa
quanto sobrou. Então a sobra é descartada e a compra é a meta cheia, porque não restou nada
aproveitável.

```
quantidade = meta
```

**2. O ingrediente acabou antes do fim do mês.** Nesse caso a meta estava baixa demais para o
consumo real, e ele não quer mais voltar para ela. Quer comprar puxando pelo que realmente foi
consumido, com uma gordurinha de 20% para não passar aperto de novo.

```
quantidade = consumo_real * 1,20
```

**3. Fluxo normal.** Sobrou alguma coisa e o ingrediente está bom. Compra-se só a diferença para
voltar à meta do início do mês.

```
quantidade = meta - estoque_atual
```

No fim, itens com quantidade zero ou negativa não entram na lista. Isso acontece quando o estoque
que sobrou já cobre a meta, ou seja, não há nada a comprar para aquele ingrediente.

Uma observação sobre a fala dele de que nunca consome mais do que tem guardado: por isso o
estoque atual nunca fica negativo, e no fluxo normal a conta nunca passa da meta.

## Formato de saída

A lista sai um item por linha, no formato pedido:

```
Comprar: 12 Kg de Farinha
Comprar: 8 L de Leite
Comprar: 30 un de Ovo
```

Quantidades inteiras aparecem sem casas decimais, para não poluir a lista. Quando o cálculo dos
20% gera um número quebrado, mostro com duas casas.

## Como rodar localmente

Você vai precisar do Python 3.10 ou superior e do Git.

**1. Clone o repositório**

```bash
git clone https://github.com/oadrianops/projeto_veloz.git
cd projeto_veloz
```

**2. Crie e ative um ambiente virtual**

No Linux ou macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

No Windows, com PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

# CASO OCORRER ERRO, EXECUTE ESSE COMANDO PARA ABRIR UMA EXCEÇÃO DE SEGURANÇA.
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

**4. Aplique as migrações**

```bash
python manage.py migrate
```

**5. Crie um usuário administrador**

É com ele que você entra no painel para cadastrar os ingredientes.

```bash
python manage.py createsuperuser
```

**6. Suba o servidor**

```bash
python manage.py runserver
```

Pronto. A lista de compras fica em http://127.0.0.1:8000/ e o painel em
http://127.0.0.1:8000/admin/.

Não é preciso configurar nada além disso. As opções sensíveis do Django saem de variáveis de
ambiente e já vêm com padrão de desenvolvimento, então o clone roda direto.

## Variáveis de ambiente

Usadas só na hospedagem. Sem elas o projeto assume os valores de desenvolvimento.

| Variável | Padrão local | Para que serve |
|---|---|---|
| `DEBUG` | `True` | Desligue em produção com `False` |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Domínios aceitos, separados por vírgula |
| `CSRF_TRUSTED_ORIGINS` | vazio | Origens HTTPS confiáveis, separadas por vírgula |
| `SECRET_KEY` | chave de desenvolvimento | Chave própria em produção |

## Como usar

Entre no painel administrativo e cadastre os ingredientes em **Ingredientes**. Cada um tem os
seguintes campos:

| Campo | O que é |
|---|---|
| Nome | O nome do ingrediente, como Farinha |
| Unidade | Como ele é medido: Kg, L, un |
| Meta | Quanto o Seu Raimundo gosta de manter no início do mês |
| Estoque atual | Quanto sobrou agora, no fim do mês |
| Consumo real | Quanto foi consumido, usado só quando o item faltou |
| Vencido | Marque se o ingrediente estragou |
| Faltou antes do fim | Marque se acabou no meio do mês |

Depois é só abrir a página inicial. A lista é recalculada a cada acesso, sempre com os dados mais
recentes do banco.

Se nenhum item precisar de compra, a página avisa que o estoque está em dia em vez de mostrar uma
lista vazia.

## Estrutura do projeto

```
projeto_veloz/
├── estoque/
│   ├── models.py                 # O modelo Ingrediente
│   ├── views.py                  # Onde mora o cálculo da reposição
│   ├── admin.py                  # Registro do modelo no painel
│   ├── urls.py                   # Rota da lista de compras
│   └── templates/estoque/
│       └── lista_compras.html    # A tela, em HTML e CSS puros
├── setup/
│   ├── settings.py               # Configurações do Django
│   └── urls.py                   # Rotas principais
├── manage.py
├── nixpacks.toml                 # Configuração do build no deploy
└── requirements.txt
```

A lógica de reposição fica na view `lista_compras`, dentro da aplicação Django. Não há script
solto fora do framework.

## Tecnologias

- Django como backend
- SQLite como banco de dados
- HTML e CSS puros no frontend, sem framework nem biblioteca
- Gunicorn e WhiteNoise na hospedagem

## O que ficou de fora

O frontend em React era diferencial e não foi feito. Preferi entregar a página em HTML e CSS bem
acabada, cumprindo o requisito obrigatório, e investir o tempo restante em deixar a lógica das
regras clara e o projeto no ar.

A hospedagem, que também era diferencial, está feita e o link está no topo deste arquivo.

## Autor

Adriano Pinheiro
