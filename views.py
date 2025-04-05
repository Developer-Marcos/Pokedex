from flask import Flask, render_template, redirect, url_for, request
from projeto import app
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def mostrar_pokemon():
    id = request.args.get('id', 1, type=int)
    pokemon = None
    error = None

    if id:
        url = f'https://pokeapi.co/api/v2/pokemon/{id}'
        resposta = requests.get(url)

        if resposta.status_code == 200:
            dados = resposta.json()

            pokemon = {
                'nome': dados['name'],
                'id': dados['id'], 
                'tipos': [t['type']['name'] for t in dados['types']],
                'altura': dados['height'],
                'peso': dados['weight'],
                'sprite': dados['sprites']['front_default']
            }
            
            species_url = dados['species']['url']
            species_resposta = requests.get(species_url)
            descricao = ''
            if species_resposta.status_code == 200:
                  species_data = species_resposta.json()
                  for entry in species_data['flavor_text_entries']:
                        if entry['language']['name'] == 'en':
                              descricao = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
                              break
                        
            pokemon['descricao'] = descricao

        else:
            error = 'Pokémon não encontrado.'

    return render_template('pokedex.html', pokemon=pokemon, error=error)

@app.route('/proximo_pokemon')
def proximo_pokemon():
    id = request.args.get('id', 1, type=int)
    if id < 1025:
        id += 1
    return redirect(url_for('mostrar_pokemon', id=id))


@app.route('/pokemon_anterior')
def pokemon_anterior():
      id = request.args.get('id', 1, type=int)
      if id != 1:
            id -= 1
      return redirect(url_for('mostrar_pokemon', id=id))