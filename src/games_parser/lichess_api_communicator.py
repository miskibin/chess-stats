from games_parser.api_communicator import ApiCommunicator


class LichessApiCommunicator(ApiCommunicator):
    BASE_URL = "https://lichess.org/api/"
    HOST = "lichess.org"

    def __get_games(self, username: str, games: int, time_class: str) -> list[dict]:
        self._logger.info(f"Collecting {games} games from lichess.org")
        headers = {"Accept": "application/x-chess-pgn"}
        params = {"max": games, "perfType": time_class, "clocks": "true"}
        url = self.BASE_URL + "games/user/" + username
        response = self.send_query(url, headers=headers, params=params)
        games = self.split_pgns(response.text)
        return games

    def get_games(self, username: str, games: int, time_class: str):
        list_of_games = self.__get_games(username, games, time_class)
        return super().games_generator(username, list_of_games)
