![example workflow](https://github.com/michalskibinski109/chess_analyse_app/actions/workflows/python-app.yml/badge.svg)

**project still under development**

# chess_analyse_app

1. [Description](#description)
2. [Installation](#installation)
3. [Usage](#usage)
4. [examples](#examples)
5. [how does it work](#how-does-it-work)

## description

Create reports from your chess games that you played on `chess.com` (in future also `lichess.org`) for free. Track your progress and improve your game. Check your win ratio per opening,
per time control,per day of the week, check in which stage of the game you are losing the most, and much more.

## installation

```bash
git clone https://github.com/michalskibinski109/chess_analyse_app.git
cd chess_analyse_app
pip install -e .
pip install -r requirements.txt
```

## usage

to run server

```bash
$env:pythonpath += python src/server/manage.py makemigrations; python src/server/manage.py migrate; python src/server/manage.py runserver
```

to run queuing system

```bash
python src/server/manage.py qcluster
```

## examples

### create report (you don't need to be logged in)

<img src="https://user-images.githubusercontent.com/77834536/199267740-acb1cbb4-ffbb-4cf8-97fb-23c199e91621.png" width="800" />

### view statistics

<img src="https://user-images.githubusercontent.com/77834536/199268054-d3fbb50d-da08-44b3-a81c-1e98cc2812db.png" width="800" />
<img src="https://user-images.githubusercontent.com/77834536/199268106-5f8f5264-4309-4e69-a57d-e95773fe332e.png" width="800" />
<img src="https://user-images.githubusercontent.com/77834536/199268132-2263e22c-d170-4edc-8f28-a145c66b5106.png" width="800" />

### You can check all reports

<img src="https://user-images.githubusercontent.com/77834536/199268209-236ae7b8-0dd8-4075-8442-25338a8cd8a1.png" width="800" />

## how does it work

1. send get request to chess.com api with given username to get all of the player games
2. convert png strings to python objects
3. convert python objects to dataframe
4. show all of information about games on charts using django web app. (In progress)

### example output for single game parsed by `games_parser` module:

```

Game:
player_elo: 1354
opponent_elo: 1433
opening: Vienna Game: Max Lange Defense
result: 0
date: 2021-12-02 11:35:59
time_control: 3+2
player_color: 0
mean_player_time_per_move: 4.99
mean_opponent_time_per_move: 4.82
moves: 57
time_class: blitz
phases: (6, 60, 114)
mistakes: [(0, 0, 0), (6, 1, 3), (0, 0, 5)]

```
