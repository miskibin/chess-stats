
![example workflow](https://github.com/michalskibinski109/chess_analyse_app/actions/workflows/python-app.yml/badge.svg)
# chess_analyse_app
! project still under development

### how does it work
1. send get request to chess.com api with given username to get all of the player games
2. convert png strings to python objects
3. convert python objects to dataframe
4. shows all of information about games on charts using django web app. (TODO)

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

You can track progress of work here. [trello dashboard](https://trello.com/b/Gj2Rr5D2/chess-app)
