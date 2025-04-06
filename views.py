from flask import Flask, render_template, redirect, url_for, request, flash
from projeto import app
import requests

@app.route('/', methods=['GET'])
def mostrar_pokemon():
    id = request.args.get('id', default=1, type=int)
    nome = request.args.get('pokemon', default=None, type=str)
    pokemon = None

    if id or nome:
        alvo = id if id else nome.lower()
        url = f'https://pokeapi.co/api/v2/pokemon/{alvo}'
        resposta = requests.get(url)

        if resposta.status_code == 200:
            dados = resposta.json()

            pokemon = {
                'nome': dados['name'],
                'id': dados['id'], 
                'tipos': [t['type']['name'] for t in dados['types']],
                'altura': dados['height'] / 10,
                'peso': dados['weight'] / 10,
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
            flash('Pokemon not found!')
            return redirect(url_for('mostrar_pokemon'))
        
    return render_template('pokedex.html', pokemon=pokemon)

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

@app.route('/buscar_pokemon', methods=['GET'])
def buscar_pokemon():
    pokemon_inserido = request.args.get('poke', '').strip().lower()

    if pokemon_inserido.isalpha():
        return redirect(url_for('mostrar_pokemon', pokemon=pokemon_inserido))
    elif pokemon_inserido.isdigit():    
        return redirect(url_for('mostrar_pokemon', id=pokemon_inserido))
    else:
        flash('Invalid data, please search for Pokemon ID or name!')
        return redirect(url_for('mostrar_pokemon'))
