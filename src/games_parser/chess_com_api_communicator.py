from datetime import datetime
import chessdotcom
from chessdotcom.types import ChessDotComError
from games_parser.api_communicator import ApiCommunicator, InvalidUsernameException


class InvalidResponseFormatException(Exception):
    pass


class ChessComApiCommunicator(ApiCommunicator):
    def __init__(self, logger, depth):
        super().__init__(logger, depth)
        self.host = "chess.com"

    def get_games(self, username: str, games: int, time_class: str):
        list_of_games = self.__get_games(username, games, time_class)
        return super().games_generator(username, list_of_games)

    def __get_joined_year(self, usr: str) -> int:
        if not usr:
            self._logger.error("No username provided")
            return []
        try:
            response = chessdotcom.get_player_profile(usr)
        except ChessDotComError as err:
            self._logger.error(f"Failed to get response from chess.com: {err.text}")
            raise err
        joined = response.json["player"]["joined"]
        year = datetime.fromtimestamp(joined).year
        return year

    def __get_chess_com_response(self, usr: str, y: int, m: int) -> list:
        try:
            resp = chessdotcom.get_player_games_by_month(usr, y, m).json
            games = resp["games"]
        except (ChessDotComError) as err:
            self._logger.error(f"Failed to get response from chess.com: {err.message}")
            raise err
        self._logger.debug(f"In {y}-{m} : {len(games)} games was played")
        return games

    def __get_games(self, usr: str, games_num: int, time_class: str) -> None:
        joined_year = self.__get_joined_year(usr)
        games = []
        for y in range(datetime.now().year, joined_year - 1, -1):
            if y == datetime.now().year:
                m = int(datetime.now().month)
            else:
                m = 12
            while m > 0:
                games_json = self.__get_chess_com_response(usr, y, m)

                for g in games_json:
                    if len(games) >= games_num:
                        return games
                    if g["time_class"] == time_class:
                        games.append(g["pgn"])
                m -= 1
        return games
