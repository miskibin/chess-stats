
![example workflow](https://github.com/michalskibinski109/chess_analyse_app/actions/workflows/python-app.yml/badge.svg)
# chess_analyse_app
! project still under development

### how does it work
1. send get request to chess.com api with given username to get all of the player games
2. convert png strings to python objects
3. convert python objects to dataframe
4. shows all of information about games on charts using django web app. (TODO)

### example output for games_parser module:
```
Game:
    time_control: 180+0
    player:
        color: Color.WHITE
        elo: 1419

    opponent:
        color: Color.BLACK
        elo: 1492

    result: Result.BLACK
    date: 2021-12-08 13:40:06
    opening: Caro-Kann Defense
    phases: (6, 22, 22)
    evaluations: [30, 54, 29, 52, -20, 0, -9, 33, 13, 16, -15, -8, -10, -9, -19, -5, -2, 71, 7, 119, 96, 702]
```


