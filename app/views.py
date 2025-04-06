from flask import Blueprint, render_template, request, flash, redirect, url_for
from .helpers import chamar_api, error_e_redirecionamento
import requests

bp = Blueprint('main', __name__)

@bp.route('/')
def mostrar_pokemon():
    id = request.args.get('id', default=1, type=int)
    pokemon = chamar_api(id, None)
    return render_template('pokedex.html', pokemon=pokemon, id=id)

@bp.route('/proximo_pokemon')
def proximo_pokemon():
    id = request.args.get('id', 1, type=int)
    if id < 1025:
        id += 1
    return redirect(url_for('main.mostrar_pokemon', id=id))

@bp.route('/pokemon_anterior')
def pokemon_anterior():
    id = request.args.get('id', 1, type=int)
    if id != 1:
        id -= 1
    return redirect(url_for('main.mostrar_pokemon', id=id))

@bp.route('/buscar_pokemon', methods=['GET'])
def buscar_pokemon():
    pokemon_inserido = request.args.get('poke', '').strip().lower()

    if not pokemon_inserido:
        return error_e_redirecionamento()

    if pokemon_inserido.replace('-', '').isalpha():
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_inserido}'
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            return redirect(url_for('main.mostrar_pokemon', id=dados['id']))
        else:
            return error_e_redirecionamento()

    if pokemon_inserido.isdigit():
        poke_id = int(pokemon_inserido)
        if 1 <= poke_id <= 1025:
            url = f'https://pokeapi.co/api/v2/pokemon/{poke_id}'
            resposta = requests.get(url)
            if resposta.status_code == 200:
                return redirect(url_for('main.mostrar_pokemon', id=poke_id))

    return error_e_redirecionamento()






