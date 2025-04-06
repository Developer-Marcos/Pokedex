from flask import Flask, render_template, redirect, url_for, request, flash
from projeto import app
import requests

app.secret_key = 'blablablaawdaw'

@app.route('/', methods=['GET'])
def mostrar_pokemon():
    id = request.args.get('id', default=None, type=int)
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

    if not pokemon_inserido:
        flash('Invalid data, please search for Pokemon ID or name!')
        return redirect(url_for('mostrar_pokemon', id=1))

    if pokemon_inserido.isalpha():
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_inserido}'
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return redirect(url_for('mostrar_pokemon', pokemon=pokemon_inserido))
        else:
            flash(f'Invalid data, please search for Pokemon ID or name!')
            return redirect(url_for('mostrar_pokemon', id=1))

    elif pokemon_inserido.isdigit():
        poke_id = int(pokemon_inserido)
        if poke_id > 0 and poke_id <= 1025:
            url = f'https://pokeapi.co/api/v2/pokemon/{poke_id}'
            resposta = requests.get(url)
            if resposta.status_code == 200:
                return redirect(url_for('mostrar_pokemon', id=poke_id))
            else:
                flash(f'Invalid data, please search for Pokemon ID or name!')
                return redirect(url_for('mostrar_pokemon', id=1))
        else:
            flash('Invalid data, please search for Pokemon ID or name!')
            return redirect(url_for('mostrar_pokemon', id=1))
    else:
        flash('Invalid data, please search for Pokemon ID or name!')
        return redirect(url_for('mostrar_pokemon', id=1))

