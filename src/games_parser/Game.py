from datetime import datetime
from src.games_parser.utils import get_field_value, get_pgn
from logging import Logger
from enum import Enum
from src.games_parser.Player import Player, Color
from stockfish import Stockfish
import numpy as np
import chess
import chess.pgn
import io


class InvalidResultException(Exception):
    pass


class Result(Enum):
    White = 0
    Black = 1
    Draw = .5
    OnGoing = -1


class Game:
    """ Class representing a game."""

    def __init__(self, pgn: str, username: str, logger: Logger, openings) -> None:
        self._logger = logger
        self._pgn = get_pgn(pgn)
        self.time_control = self.__set_time_control()
        color = bool(self.__set_color(username))
        self.player = Player(pgn, Color(color).value,
                             self.time_control, logger)
        self.opponent = Player(pgn, not Color(
            color).value, self.time_control, logger)
        self.result = self.__set_result()
        self.date = self.__set_date()
        self.opening, moves = self.set_opening(pgn, openings)
        self.phases = self.__set_phases(moves + 2, pgn)
        self.evaluations = self.__set_evaluations(pgn)
        print(self.__mistakes_per_phase(pgn))
        print(self.phases)
        print(self.player.color)
    PIECE_VALUES = {
        'p': 1,
        'P': 1,
        'n': 3,
        'N': 3,
        'q': 9,
        'Q': 9,
        'r': 5,
        'R': 5,
        'b': 3,
        'B': 3,
        'k': 0,
        'K': 0
    }

    def __set_phases(self, middlegame, pgn):
        game = chess.pgn.read_game(io.StringIO(
            pgn), Visitor=chess.pgn.BoardBuilder)
        board = chess.Board()
        for index, move in enumerate(game.move_stack):
            board.push(move)
            points = sum([self.PIECE_VALUES[str(i)]
                         for i in board.piece_map().values()])
            if points < 28:
                if index > middlegame:
                    return (middlegame, index, len(game.move_stack))
                return (middlegame, middlegame, len(game.move_stack))
        return (middlegame, len(game.move_stack), len(game.move_stack))

    @staticmethod
    def set_opening(pgn, openings):
        board = chess.pgn.read_game(io.StringIO(
            pgn), Visitor=chess.pgn.BoardBuilder)
        [board.pop() for _ in range(len(board.move_stack) - len(openings))]
        for i in range(len(board.move_stack) - 1, -1, -1):
            for opening in openings[i]:
                if opening['fen'] in board.fen():
                    return opening['name'], len(board.move_stack)
            board.pop()
        return None, 0

    def __set_color(self, username) -> Color:
        if username in get_field_value(self._pgn.headers, "White"):
            return Color.White
        return Color.Black

    def __set_result(self) -> Result:
        RESULT = {
            "1-0": 1,
            "0-1": 0,
            "1/2-1/2": 0.5,
            "*": -1
        }
        result = get_field_value(self._pgn.headers, "Result")
        try:
            return Result(RESULT.get(result, -1))
        except KeyError as exc:
            self._logger.error("Invalid result: " + result)
            raise InvalidResultException("Invalid result: " + result) from exc

    def __set_date(self):
        date = get_field_value(self._pgn.headers, "UTCDate")
        time = get_field_value(self._pgn.headers, "UTCTime")
        date_time = datetime.strptime(date + ' ' + time, '%Y.%m.%d %H:%M:%S')
        return date_time

    def __set_time_control(self):
        temp = get_field_value(self._pgn.headers, "TimeControl")
        if '/' in temp:  # daily time control
            temp = temp.split('/')[1]
        if '+' not in temp:
            temp = temp + '+0'
        if len(temp.split('+')) != 2:
            self._logger.error("Invalid time control: " + temp)
            raise Exception("Invalid time control: " + temp)
        return temp

    def __set_evaluations(self, pgn):
        stockfish = Stockfish('stockfish.exe', depth=14)
        board = chess.pgn.read_game(io.StringIO(
            pgn), Visitor=chess.pgn.BoardBuilder)
        evaluations = []
        for move in board.move_stack:
            stockfish.make_moves_from_current_position([move.uci()])
            eval = stockfish.get_evaluation()
            if eval['type'] == 'mate':
                eval = eval['value']*1000
            else:
                eval = eval['value']
            if abs(eval) > 1000:
                eval = eval/abs(eval)*1000
            evaluations.append(eval)
            print(move)
        return evaluations

    def __mistakes_per_phase(self, pgn):
        """
        returns [
            opening(inaccuraces, mistakes, blunders),
            middlegame(inaccuraces, mistakes, blunders), 
            endgame(inaccuraces, mistakes, blunders)
            ]
        """
        game = chess.pgn.read_game(io.StringIO(
            pgn), Visitor=chess.pgn.BoardBuilder)
        moves = [g for g in game.move_stack]
        mistakes = []
        INACCURACY, MISTAKE, BLUNDER = 50, 120, 200
        prev = 0
        for phase in self.phases:
            inacc, mist, blund = 0, 0, 0
            for move_num in range(max(prev, 1), phase):
                if (move_num + self.player.color) % 2 == 0:
                    loss = -((-self.player.color*2) + 1) * \
                        (self.evaluations[move_num] -
                         self.evaluations[move_num - 1])
                    if loss > BLUNDER:
                        blund += 1
                        print(loss, moves[move_num])
                    elif loss > MISTAKE:
                        mist += 1
                        print(loss, moves[move_num])
                    elif loss > INACCURACY:
                        inacc += 1
                        print(loss, moves[move_num])
            mistakes.append((inacc, mist, blund))
            prev = phase
        return mistakes

    @staticmethod
    def get_time_class(t_c: str) -> str:
        time = int(t_c.split('+')[0])
        if time < 3:
            return 'bullet'
        if time < 10:
            return 'blitz'
        if time < 30:
            return 'rapid'
        return 'classical'

    def asdict(self) -> dict:
        temp = self.time_control.split('+')
        t_c = str(int(temp[0])//60) + '+' + str(temp[1])

        return {
            'player_elo': self.player.elo,
            'opponent_elo': self.opponent.elo,
            'opening': self.opening,
            'result': self.result.value,
            'date': self.date,
            'time_control': t_c,
            'player_color': self.player.color.value,
            'mean_player_time_per_move': round(np.mean(self.player.time_per_move), 2),
            'mean_opponent_time_per_move': round(np.mean(self.opponent.time_per_move), 2),
            'moves': max(len(self.player.time_per_move), len(self.opponent.time_per_move)),
            'time_class': self.get_time_class(t_c),
            'phases': self.phases,
            'mistakes': self.__mistakes_per_phase()

        }

    def __str__(self) -> str:
        tree = str(type(self).__name__) + ':\n'
        for key, val in self.__dict__.items():
            if key[0] != '_':
                tree += '\t' + key + ': ' + str(val) + '\n'
        return tree
