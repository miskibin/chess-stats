import requests
from games_parser.api_communicator import ApiCommunicator, InvalidUsernameException
from logging import Logger


class LichessApiCommunicator(ApiCommunicator):
    def __init__(self, logger: Logger, depth: int = 10) -> None:
        super().__init__(logger, depth)
        self.base_url = "https://lichess.org/api/"
        self.host = "lichess.org"

    def __get_games(self, username: str, games: int, time_class: str) -> list[dict]:
        self._logger.info(f"Collecting {games} games from lichess.org")
        headers = {"Accept": "application/x-chess-pgn"}
        params = {"max": games, "perfType": time_class, "clocks": "true"}
        url = self.base_url + "games/user/" + username
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            self._logger.error(f"Invalid username: {username}: {response.status_code}")
            raise InvalidUsernameException from errh
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            self._logger.error(f"Error while getting games from lichess.org: {e}")
            raise SystemExit(e)
        games = response.text.split("\n\n\n")
        return games

    def get_games(self, username: str, games: int, time_class: str):
        list_of_games = self.__get_games(username, games, time_class)[:-1]
        return super().games_generator(username, list_of_games)
