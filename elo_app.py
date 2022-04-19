from elo_system import EloSystem

from flask import Flask, render_template, request, redirect, url_for
import datetime
from zoneinfo import ZoneInfo
import json
import os

app = Flask(__name__)
elo = EloSystem(base_elo = 1200, k = 42)

def save():
    ratings = elo.get_overall_list()
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(ratings, f)

@app.route('/')
def hello_world():
    ratings = elo.get_overall_list()
    if not ratings and os.path.isfile("data.json"):
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        for row in data:
                elo.add_player(row["player"], row["elo"])
    players = [d['player'] for d in ratings]
    return render_template("index.html", ratings=ratings, players=players)

@app.route('/add_player', methods=["GET", "POST"])
def add_player():
    ratings = elo.get_overall_list()
    players = [d['player'] for d in ratings]
    if request.method == "POST":
        player = request.form["player"][:20].strip().capitalize()
        if player != "" and player not in players:
            elo.add_player(player)
            save()
        # return f'Player added {request.form["player"]}'
    return redirect(url_for('hello_world'))

@app.route('/record_match', methods=["GET", "POST"])
def record_match():
    if request.method == "POST":
        p1 = request.form["winner"][:20].strip().capitalize().replace("Remy", "Rémy").replace("Gael", "Gaël")
        p2 = request.form["loser"][:20].strip().capitalize().replace("Remy", "Rémy").replace("Gael", "Gaël")

        elo.record_match(p1, p2, winner = str(p1))
        record = {
            "time" : datetime.datetime.now(ZoneInfo("Europe/Brussels")).isoformat(),
            "winner": p1,
            "loser": p2
        }
        if os.path.isfile("history.json"):
            with open('history.json', 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = []
        history.append(record)
        with open('history.json', 'w', encoding='utf-8') as f:
            json.dump(history, f)
        # return 'Match added'
        save()
    return redirect(url_for('hello_world'))

@app.route('/history')
def history():
    if os.path.isfile("history.json"):
        with open('history.json', 'r', encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = []
    return render_template("history.html", history=history)

@app.route('/get_elo/<username>')
def get_elo(username):
    return elo.get_player_elo(username)

@app.route('/get_elo_list')
def get_elo_list():
    return elo.get_overall_list()

@app.route('/get_player_rank/<username>')
def get_player_rank(username):
    return elo.get_player_rank(username)

@app.route('/get_player_count')
def get_player_count():
    return elo.get_player_count()

@app.route('/get_players_with_rank/<rank>')
def get_players_with_rank(rank):
    return elo.get_players_with_rank(rank)
