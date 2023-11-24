# -*- coding: utf-8 -*-

from GamePlay import GamePlay
from flask import Flask


game = GamePlay(3)
session_id = game.session_id
app = Flask(__name__)

@app.route("/")
def home():
    a = ''
    for player in game.players:
        a += '<p>\t\t' + player.id + '</p>\n'
    return a


@app.route("/get-players")
def get_players():
    return [player.id for player in game.players]

@app.route("/get-table-info")
def get_table_info():
    player_details = {}
    for player in game.players:
        player_details[player.id] = player.info_dict
    return {
        'session_id': session_id,
        'n_players': len(get_players()),
        'player_details': player_details