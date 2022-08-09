import io
import chess.pgn


class InvalidJsonFormatException(Exception):
    pass


def get_field_value(json_data, field_name):
    """
    Get the value of a field from a json object.
    """
    try:
        value = json_data[field_name]
    except KeyError as exc:
        raise InvalidJsonFormatException(field_name) from exc
    return value


def get_pgn(pgn: str) -> chess.pgn.Game:
    """Get the headers from a pgn file."""
    pgn = io.StringIO(pgn)
    game = chess.pgn.read_game(pgn)
    return game

if __name__ == '__main__':
    pgn = "[Event \"Live Chess\"]\n[Site \"Chess.com\"]\n[Date \"2021.01.31\"]\n[Round \"-\"]\n[White \"MikioHayase\"]\n[Black \"Barabasz60\"]\n[Result \"0-1\"]\n[CurrentPosition \"5r2/7k/4R1pp/Q7/3B4/1P6/P5B1/5rK1 w - -\"]\n[Timezone \"UTC\"]\n[ECO \"A01\"]\n[ECOUrl \"https://www.chess.com/openings/Nimzowitsch-Larsen-Attack-Classical-Variation-2.Bb2\"]\n[UTCDate \"2021.01.31\"]\n[UTCTime \"21:39:38\"]\n[WhiteElo \"1053\"]\n[BlackElo \"1073\"]\n[TimeControl \"60\"]\n[Termination \"Barabasz60 won on time\"]\n[StartTime \"21:39:38\"]\n[EndDate \"2021.01.31\"]\n[EndTime \"21:41:54\"]\n[Link \"https://www.chess.com/game/live/6409516118\"]\n\n1. b3 {[%clk 0:01:00]} 1... d5 {[%clk 0:00:59.9]} 2. Bb2 {[%clk 0:00:59.9]} 2... e6 {[%clk 0:00:59.8]} 3. e3 {[%clk 0:00:59.8]} 3... c5 {[%clk 0:00:59.1]} 4. g3 {[%clk 0:00:59.7]} 4... Nc6 {[%clk 0:00:58.6]} 5. Bg2 {[%clk 0:00:59.6]} 5... h6 {[%clk 0:00:57.3]} 6. Ne2 {[%clk 0:00:59.5]} 6... Nf6 {[%clk 0:00:57]} 7. O-O {[%clk 0:00:59.4]} 7... a6 {[%clk 0:00:56.2]} 8. h3 {[%clk 0:00:59.3]} 8... Be7 {[%clk 0:00:55.7]} 9. g4 {[%clk 0:00:59.2]} 9... O-O {[%clk 0:00:55.3]} 10. Ng3 {[%clk 0:00:58.3]} 10... Bd7 {[%clk 0:00:54.9]} 11. f4 {[%clk 0:00:57.7]} 11... Qc7 {[%clk 0:00:54.4]} 12. d3 {[%clk 0:00:57.1]} 12... b5 {[%clk 0:00:52.2]} 13. Nd2 {[%clk 0:00:57]} 13... c4 {[%clk 0:00:51.3]} 14. Nf3 {[%clk 0:00:56.9]} 14... cxb3 {[%clk 0:00:50.3]} 15. cxb3 {[%clk 0:00:55.3]} 15... Bc5 {[%clk 0:00:47.4]} 16. d4 {[%clk 0:00:53.7]} 16... Bb6 {[%clk 0:00:45.8]} 17. Ne5 {[%clk 0:00:52.7]} 17... Nxe5 {[%clk 0:00:44.7]} 18. fxe5 {[%clk 0:00:52.6]} 18... Ne8 {[%clk 0:00:43.6]} 19. Nh5 {[%clk 0:00:50.1]} 19... g6 {[%clk 0:00:39.6]} 20. Nf6+ {[%clk 0:00:48]} 20... Nxf6 {[%clk 0:00:37.9]} 21. exf6 {[%clk 0:00:47.9]} 21... Rac8 {[%clk 0:00:35.7]} 22. Qd3 {[%clk 0:00:41.7]} 22... Kh7 {[%clk 0:00:34.8]} 23. h4 {[%clk 0:00:39.5]} 23... a5 {[%clk 0:00:31.8]} 24. h5 {[%clk 0:00:38.6]} 24... e5 {[%clk 0:00:27]} 25. hxg6+ {[%clk 0:00:35.3]} 25... fxg6 {[%clk 0:00:26.2]} 26. dxe5 {[%clk 0:00:30.1]} 26... Bxg4 {[%clk 0:00:23]} 27. e6 {[%clk 0:00:23.3]} 27... d4 {[%clk 0:00:17.3]} 28. f7 {[%clk 0:00:20.2]} 28... Qe5 {[%clk 0:00:12.1]} 29. exd4 {[%clk 0:00:16.8]} 29... Bxd4+ {[%clk 0:00:10.7]} 30. Bxd4 {[%clk 0:00:15.4]} 30... Qxe6 {[%clk 0:00:07.3]} 31. Rae1 {[%clk 0:00:12.6]} 31... Qxf7 {[%clk 0:00:06.1]} 32. Rxf7+ {[%clk 0:00:11]} 32... Rxf7 {[%clk 0:00:06]} 33. Qxb5 {[%clk 0:00:08.8]} 33... Rcf8 {[%clk 0:00:05.1]} 34. Qxa5 {[%clk 0:00:05.2]} 34... Be6 {[%clk 0:00:03.3]} 35. Rxe6 {[%clk 0:00:01.7]} 35... Rf1+ {[%clk 0:00:01.8]} 0-1\n"
    pgn = get_pgn(pgn)
    start_time, add_time = 60, 0
    time_left = [start_time, start_time]
    times = ([], [])
    for index, move in enumerate(pgn.mainline()):
        times[index % 2].append(round(time_left[index % 2] - move.clock() + add_time,2))
        time_left[index % 2] = move.clock()
    print(times)