![example workflow](https://github.com/michalskibinski109/chess_analyse_app/actions/workflows/python-app.yml/badge.svg)

# chess_analyse_app

! project still under development

### how does it work

1. send get request to chess.com api with given username to get all of the player games
2. convert png strings to python objects
3. convert python objects to dataframe
4. shows all of information about games on charts using django web app. (In progress)

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
# view images from the GUI
![image](https://user-images.githubusercontent.com/77834536/193069968-3149afd5-29af-4152-9d20-c2c5dfdf2c29.png)
![image](https://user-images.githubusercontent.com/77834536/193069693-4500db90-2ad3-4cc7-a3eb-4b2aa5213d88.png)
![image](https://user-images.githubusercontent.com/77834536/193069709-86ba6e3b-bfc3-4d03-8a2e-d9a24fd56b9e.png)
![image](https://user-images.githubusercontent.com/77834536/193069813-0123b543-da88-415b-a6b6-63137809cddc.png)
