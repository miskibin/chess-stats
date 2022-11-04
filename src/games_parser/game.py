import io
from datetime import datetime
from enum import Enum
from logging import Logger
import chess
import chess.pgn
import numpy as np
from stockfish import Stockfish
from games_parser.player import Color, Player
from games_parser.utils import get_field_value, get_pgn
from typing import Union


class InvalidResultException(Exception):
    pass


class Result(Enum):
    WHITE = 0
    BLACK = 1
    DRAW = 0.5
    ON_GOING = -1


class Game:
    """Class representing a game."""

    def __init__(
        self,
        pgn: str,
        username: str,
        logger: Logger,
        openings: list,
        stockfish: Stockfish = None,
    ) -> None:
        self._logger = logger
        self._pgn = get_pgn(pgn)
        self.time_control = self.__set_time_control()
        color = bool(self.__set_color(username))
        self.player = Player(pgn, Color(color).value, self.time_control, logger)
        self.opponent = Player(pgn, not Color(color).value, self.time_control, logger)
        self.result = self.__set_result()
        self.date = self.__set_date()
        self.opening, moves = self.__set_opening(pgn, openings)
        self.phases = self.__set_phases(moves + 2, pgn)
        self.evaluations = self.__set_evaluations(pgn, stockfish)

    INACCURACY, MISTAKE, BLUNDER = 50, 120, 200
    RESULT = {"1-0": 0, "0-1": 1, "1/2-1/2": 0.5, "*": -1}
    PIECE_VALUES = {
        "p": 1,
        "P": 1,
        "n": 3,
        "N": 3,
        "q": 9,
        "Q": 9,
        "r": 5,
        "R": 5,
        "b": 3,
        "B": 3,
        "k": 0,
        "K": 0,
    }

    def __set_phases(self, middlegame: int, pgn: str) -> list:
        """
        Args:
            middlegame (int): moment when middle game starts. We assume that when posiotion
            is not in opening book, it is middle game.
            pgn (str):

        Returns:
            list: move when phase ends. [opening, middlegame, endgame]
        """
        game = chess.pgn.read_game(io.StringIO(pgn), Visitor=chess.pgn.BoardBuilder)
        board = chess.Board()
        for index, move in enumerate(game.move_stack):
            try:
                board.push(move)
            except (ValueError, AssertionError) as exc:
                self._logger.error(
                    f"Invalid move {move} in game played {self.date} {exc}"
                )
                raise exc
            points = sum(self.PIECE_VALUES[str(i)] for i in board.piece_map().values())
            if points < 28:  # if more it is endgame
                if index > middlegame:
                    return (middlegame, index, len(game.move_stack))
                self._logger.debug(
                    f"there is no middle game in game played {self.date}"
                )
                return (middlegame, middlegame, len(game.move_stack))
        return (middlegame, len(game.move_stack), len(game.move_stack))

    def __set_opening(self, pgn: str, openings: list) -> tuple:
        """Method to set opening of the game. It uses opening book to find opening.
        Highly optimized.
        Args:
            pgn (str): _description_
            openings (list): _description_

        Returns:
            tuple: (opening_name, moves(this is needed for `__set_phases` method))
        """
        board = chess.pgn.read_game(io.StringIO(pgn), Visitor=chess.pgn.BoardBuilder)
        for _ in range(len(board.move_stack) - len(openings)):
            board.pop()
        for i in range(len(board.move_stack) - 1, -1, -1):
            for opening in openings[i]:
                if opening["fen"] in board.fen():
                    return opening["name"], len(board.move_stack)
            board.pop()
        self._logger.warning(f"there is no opening in game played {self.date}")
        return None, 0

    def __set_color(self, username: str) -> Color:
        if username in get_field_value(self._pgn.headers, "White"):
            return Color.WHITE
        return Color.BLACK

    def __set_result(self) -> Result:
        result = get_field_value(self._pgn.headers, "Result")
        try:
            return Result(self.RESULT.get(result, -1))
        except KeyError as exc:
            self._logger.error("Invalid result: " + result)
            raise InvalidResultException("Invalid result: " + result) from exc

    def __set_date(self) -> datetime:
        date = get_field_value(self._pgn.headers, "UTCDate")
        time = get_field_value(self._pgn.headers, "UTCTime")
        date_time = datetime.strptime(date + " " + time, "%Y.%m.%d %H:%M:%S")
        return date_time

    def __set_time_control(self) -> str:
        temp = get_field_value(self._pgn.headers, "TimeControl")
        if "/" in temp:  # daily time control
            temp = temp.split("/")[1]
        if "+" not in temp:
            temp = temp + "+0"
        if len(temp.split("+")) != 2:
            self._logger.error("Invalid time control: " + temp)
            raise Exception("Invalid time control: " + temp)
        return temp

    def __set_evaluations(self, pgn: str, stockfish: Union[Stockfish, None]) -> list:
        """Method to set evaluations of the game. It uses stockfish to find evaluations.
        Returns:
            list with evaluations for every move.
        Note:
            Stockfish is not perfect, so it can make mistakes. :(
            If stockfish is null return list of zeros.
        """
        board = chess.pgn.read_game(io.StringIO(pgn), Visitor=chess.pgn.BoardBuilder)
        if not stockfish:
            return len(board.move_stack) * [0]
        evaluations = []
        stockfish.set_position()
        for move in board.move_stack:
            stockfish.make_moves_from_current_position([move.uci()])
            evaluation = stockfish.get_evaluation()
            if evaluation["type"] == "mate":
                evaluation = evaluation["value"] * 1000
            else:
                evaluation = evaluation["value"]
            if abs(evaluation) > 1000:
                evaluation = evaluation / abs(evaluation) * 1000
            evaluations.append(evaluation)
        return evaluations

    def __mistakes_per_phase(self):
        """
        Returns [
            opening(inaccuraces, mistakes, blunders),
            middlegame(inaccuraces, mistakes, blunders),
            endgame(inaccuraces, mistakes, blunders)
            ]
        """
        mistakes = []

        prev = 0
        for phase in self.phases:
            inacc, mist, blund = 0, 0, 0
            for move_num in range(max(prev, 1), min(phase, len(self.evaluations))):
                if (move_num + self.player.color) % 2 == 0:
                    loss = -((-self.player.color * 2) + 1) * (
                        self.evaluations[move_num] - self.evaluations[move_num - 1]
                    )
                    if loss > self.BLUNDER:
                        blund += 1
                    elif loss > self.MISTAKE:
                        mist += 1
                    elif loss > self.INACCURACY:
                        inacc += 1
            mistakes.append((inacc, mist, blund))
            prev = phase
        return mistakes

    @staticmethod
    def get_time_class(t_c: str) -> str:
        time = int(t_c.split("+")[0])
        if time < 3:
            return "bullet"
        if time < 10:
            return "blitz"
        if time < 30:
            return "rapid"
        return "classical"

    def asdict(self) -> dict:
        """Method returns all data about game  .
        Returns:
            `player_elo` (int): elo of the player
            `opponent_elo` (int): elo of the opponent
            `opening` (str): opening of the game
            `short_opening` (str): eg. `Ruy Lopez: Open` -> `Ruy Lopez`
            `result` (Result): result of the game
            `date` (datetime): date of the game
            `time_control` (str): time control of the game
            `player_color` (Color): color of the player
            `mean_player_time_per_move` (float): mean time of the player per move
            `mean_opponent_time_per_move` (float): mean time of the opponent per move
            `moves` (int): number of moves in the game
            `time_class` (str): time class of the game
            `phases` (tuple): phases of the game
            `mistakes` (tuple): mistakes of the player in phases of the game
        """
        temp = self.time_control.split("+")
        t_c = str(int(temp[0]) // 60) + "+" + str(temp[1])
        if not self.opening:
            short_opening = None
        else:
            short_opening = self.opening.split(":")[0]
        return {
            "player_elo": self.player.elo,
            "opponent_elo": self.opponent.elo,
            "opening": self.opening,
            "short_opening": short_opening,
            "result": self.result.value,
            "date": self.date,
            "time_control": t_c,
            "player_color": self.player.color.value,
            "mean_player_time_per_move": round(np.mean(self.player.time_per_move), 2),
            "mean_opponent_time_per_move": round(
                np.mean(self.opponent.time_per_move), 2
            ),
            "moves": max(
                len(self.player.time_per_move), len(self.opponent.time_per_move)
            ),
            "time_class": self.get_time_class(t_c),
            "phases": self.phases,
            "mistakes": self.__mistakes_per_phase(),
        }

    def __str__(self) -> str:
        tree = str(type(self).__name__) + ":\n"
        for key, val in self.asdict().items():
            if key[0] != "_":
                tree += "\t" + key + ": " + str(val) + "\n"
        return tree
