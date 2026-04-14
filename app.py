from flask import Flask, abort, render_template, request, redirect, url_for
from acesso_url import cardapio_dos_restaurantes

app = Flask(__name__)

cardapio_criado_na_web = {}

def cardapio_ou_erro():
    cardapio = cardapio_dos_restaurantes()
    if not cardapio:
        abort(503, description='Não foi possível carregar os dados dos restaurantes.')
    return cardapio

def cardapio_completo():
    base = cardapio_ou_erro()
    completo = {}
    completo.update(base)

    for restaurante, itens in cardapio_criado_na_web.items():
        if restaurante in completo:
            completo[restaurante] = completo[restaurante] + itens
        else:
            completo[restaurante] = itens

    return completo
    
    


@app.route('/', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':    
        restaurante = request.form.get('restaurante_nome').strip() 
        prato = request.form.get('prato_nome').strip()
        preco = request.form.get('preco_nome').strip()
        descricao = request.form.get('descricao_nome').strip()

        print(f'{restaurante} | {prato} | {preco} | {descricao}')
    
        if restaurante and prato:
            if restaurante not in cardapio_criado_na_web:
                cardapio_criado_na_web[restaurante] = []

            if restaurante in cardapio_criado_na_web:
                cardapio_criado_na_web[restaurante].append({ 
                   "item": prato,
                   "price": preco,
                   "description": descricao
                })

        return redirect(url_for('inicio'))

    cardapio = cardapio_completo()

    restaurantes = sorted(cardapio.keys())
    escolha = request.args.get('restaurante')
    itens = []
    titulo = 'Cardápios'
    subtitulo = 'Escolha um restaurante na lista'
    selecionado = None


    if escolha:
        if escolha not in cardapio:
            abort(404, description='Restaurante não encontrado.')
        
        itens = cardapio[escolha]
        titulo = escolha
        subtitulo = 'Cardápio'
        selecionado = escolha

    return render_template(
        'lista.html',
        titulo = titulo,
        subtitulo = subtitulo,
        itens = itens,
        restaurantes = restaurantes,
        selecionado = selecionado
    )


if __name__ == '__main__':
    app.run(debug=True)

