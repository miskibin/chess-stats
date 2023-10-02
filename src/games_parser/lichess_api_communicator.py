from games_parser.api_communicator import ApiCommunicator
import urllib


class LichessApiCommunicator(ApiCommunicator):
    BASE_URL = "https://lichess.org/api"
    HOST = "lichess.org"

    def __get_games(self, username: str, games: int, time_class: str) -> list[dict]:
        self._logger.info(f"Collecting {games} games from lichess.org")
        headers = {"Accept": "application/x-chess-pgn"}
        params = {"max": games, "perfType": time_class, "clocks": "true"}
        url = self.BASE_URL + "/games/user/" + username
        self._logger.info(f"Sending request to {url}")
        response = self.send_query(url, headers=headers, params=params)
        games = self.split_pgns(response.text)
        return games

    def get_valid_username(self, username: str) -> None | str:
        url = urllib.parse.urljoin(self.BASE_URL, f"/api/user/{username}")
        headers = {"Accept": "application/json"}
        try:
            res = self.send_query(url, headers=headers)
        except Exception as e:
            return None
        return res.json()["username"]

    def get_games(self, username: str, games: int, time_class: str):
        list_of_games = self.__get_games(username, games, time_class)
        return super().games_generator(username, list_of_games)


if __name__ == "__main__":
    from pprint import pprint
    from easy_logs import get_logger

    lichess = LichessApiCommunicator(get_logger())
    valid = lichess.get_games("michal", 1, "blitz")
    pprint(valid)
