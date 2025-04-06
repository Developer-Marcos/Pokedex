from flask import render_template, redirect, url_for, request
from projeto import app
from helpers import chamar_api, error_e_redirecionamento
import requests

app.secret_key = 'so_serve_para_exibir_as_mensagens_flash'

@app.route('/', methods=['GET'])
def mostrar_pokemon():
    id = request.args.get('id', default=None, type=int)
    nome = request.args.get('pokemon', default=None, type=str)
    
    pokemon = chamar_api(id=id, nome=nome)

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
        return error_e_redirecionamento()

    if pokemon_inserido.replace('-', '').isalpha():
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_inserido}'
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return redirect(url_for('mostrar_pokemon', pokemon=pokemon_inserido))
        else:
            return error_e_redirecionamento()

    if pokemon_inserido.isdigit():
        poke_id = int(pokemon_inserido)
        if 1 <= poke_id <= 1025:
            url = f'https://pokeapi.co/api/v2/pokemon/{poke_id}'
            resposta = requests.get(url)
            if resposta.status_code == 200:
                return redirect(url_for('mostrar_pokemon', id=poke_id))
    
    return error_e_redirecionamento()


