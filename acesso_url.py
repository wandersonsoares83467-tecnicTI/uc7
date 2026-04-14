import requests
import json

url =  'https://guilhermeonrails.github.io/api-restaurantes/restaurantes.json'
resposta = requests.get(url)

def cardapio_dos_restaurantes():
    if resposta.status_code == 200:
        dados_json = resposta.json()
        dados_restaurantes = {}


        for item in dados_json:
            nome_do_restaurante = item["Company"]
            # print('-----')
            # print(nome_do_restaurante)

            if nome_do_restaurante not in dados_restaurantes:
                dados_restaurantes[nome_do_restaurante]=[]

            dados_restaurantes[nome_do_restaurante].append({
                "item": item['Item'],
                "price": item['price'],
                "description": item['description']
            })

        return dados_restaurantes
    
    else:
        print(f'Deu ruim. Site não encontrado. Erro código: {resposta.status_code}')



        