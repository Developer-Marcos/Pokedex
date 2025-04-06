from flask import redirect, url_for, flash
import requests
from functools import lru_cache

@lru_cache(maxsize=128)
def buscar_dados_pokemon(alvo):
    url = f'https://pokeapi.co/api/v2/pokemon/{alvo}'
    resposta = requests.get(url, timeout=5)
    resposta.raise_for_status()
    return resposta.json()

@lru_cache(maxsize=128)
def buscar_descricao_pokemon(url):
    resposta = requests.get(url, timeout=5)
    resposta.raise_for_status()
    return resposta.json()

def chamar_api(id, nome):
    pokemon = None
    if id or nome:
        alvo = id if id else nome.lower()

        try:
            dados = buscar_dados_pokemon(alvo)
        except requests.RequestException:
            return None

        pokemon = {
            'nome': dados['name'],
            'id': dados['id'],
            'tipos': [t['type']['name'] for t in dados['types']],
            'altura': dados['height'] / 10,
            'peso': dados['weight'] / 10,
            'sprite': dados['sprites']['front_default']
        }

        descricao = ''
        try:
            species_data = buscar_descricao_pokemon(dados['species']['url'])
            for entry in species_data['flavor_text_entries']:
                if entry['language']['name'] == 'en':
                    descricao = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
                    descricao = descricao.replace('POKéMON', 'Pokémon')
                    break
        except requests.RequestException:
            descricao = 'No description available.'

        pokemon['descricao'] = descricao
        return pokemon

def error_e_redirecionamento():
    flash('Invalid data, please search for Pokemon ID or name!')
    return redirect(url_for('main.mostrar_pokemon', id=1))

