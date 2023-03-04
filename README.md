![example workflow](https://github.com/michalskibinski109/chess_analyse_app/actions/workflows/python-app.yml/badge.svg)

**project still under development**

# chess_analyse_app

1. [Description](#description)
2. [Installation](#installation)
3. [Usage](#usage)
4. [examples](#examples)
5. [how does it work](#how-does-it-work)

## description

Create reports from your chess games that you played on `chess.com` and `lichess.org` for free. Track your progress and improve your game. Check your win ratio per opening,
per time control,per day of the week, check in which stage of the game you are losing the most, and much more.

## installation


```bash
git clone https://github.com/michalskibinski109/chess_analyse_app.git
cd chess_analyse_app
pip install -e .
pip install -r requirements.txt
```

### Optionall

If you want stockfish engine to analyze your app and enable some more features, you need to download it from [here](https://stockfishchess.org/download/) and put it in the project folder.

## usage

to initialize database (you need to do it only once)

```bash
python src/server/manage.py makemigrations; python src/server/manage.py migrate
```

to run server

```bash
python src/server/manage.py runserver
```

to run queuing system

```bash
python src/server/manage.py qcluster
```

## examples

### create report (you don't need to be logged in)

<img src="https://user-images.githubusercontent.com/77834536/199975224-dcf98a81-eac0-4f77-8c9c-0231444d1744.png" width="800" />

### view statistics

<img src="https://user-images.githubusercontent.com/77834536/199974885-1cf19160-a676-452c-a584-df9b2662dc40.png" width="800" />
<img src="https://user-images.githubusercontent.com/77834536/199974986-d3b0fe91-e5a0-4953-bf27-4834a755a260.png" width="800" />
<img src="https://user-images.githubusercontent.com/77834536/199975051-ab51dd34-0cd5-4cfa-9d0f-d2d43785f252.png" width="800" />

### You can check all reports...

<img src="https://user-images.githubusercontent.com/77834536/199975124-7fa990d8-4587-4774-b079-c68efe9900bd.png" width="800" />

### ... and get list of games that are in report

<img src="https://user-images.githubusercontent.com/77834536/199975295-0f1bf105-18c9-41bd-bcb0-0eb00a6ee0d6.png" width="800" />

## how does it work

1. send get request to chess.com api with given username to get all of the player games
2. convert png strings to python objects
3. convert python objects to dataframe
4. show all of information about games on charts using django web app. (In progress)

### example output for single game parsed by `games_parser` module:

```
Game:
  player_elo: 1399
  opponent_elo: 1335
  opening: Bishop's Opening: Vienna Hybrid
  short_opening: Bishop's Opening
  result: 0
  date: 2022-10-05 16:23:40
  time_control: 5+5
  player_color: 0
  mean_player_time_per_move: 6.0
  mean_opponent_time_per_move: 7.01
  moves: 24
  time_class: blitz
  phases: (9, 47, 47)
  mistakes: [(0, 2, 0), (1, 1, 5), (0, 0, 0)]
```

- `phases` - tuple of 3 values, first value is number of moves in opening, second value is number of moves in middle game, third value is number of moves in end game
- `mistakes` - tuple of 3 values, first value is number of mistakes in opening, second value is number of mistakes in middle game, third value is number of mistakes in end game


### architecture

```mermaid
---
title: Games parser 
---
classDiagram

class ApiCommunicator
class ChessComCommunicator
class LichessCommunicator

class CommunicatorFactory

class Game
class Player

CommunicatorFactory --> ApiCommunicator: create

subgraph api_communicator
  ApiCommunicator <|-- ChessComCommunicator
  ApiCommunicator <|-- LichessCommunicator
  ApiCommunicator o-- Game
  Game o-- Player
end
```


### database


```mermaid
---
title: Chess analyse app database
---

erDiagram
REPORT ||--|{ GAME : has
REPORT {
    
    string chess_com_username
    string lichess_username
    string time_class
    int games_num
    int analyzed_games
    int engine_depth
}
GAME {
    int player_elo
    int opponent_elo
    string opening
    string short_opening
    int result
    datetime date
    string time_control
    int player_color
    int mean_player_time_per_move
    int mean_opponent_time_per_move
    int moves
    string time_class
    json phases
    json mistakes
    datetime created
}
```




## Note

In this project I use logger from my other package. You can check it [here](https://github.com/michalskibinski109/miskibin) if you want to use collored logs in your project.
