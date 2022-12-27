from logging import Logger
from time import time


class ConclusionsMaker:
    """
    This class is used to create queries for the report.
    It is as most generic as possible.
    To add a new query, add a method that starts with "get_" and returns the data.
    """

    def __init__(self, data: dict, logger: Logger) -> None:
        self.logger = logger
        self.data = data
        self.get_methods = [
            method
            for method in dir(self)
            if callable(getattr(self, method)) and method.startswith("get")
        ]

    def asdict(self) -> dict:
        """
        This method is used to get the data from the queries.
        it will return a dict with the name of the method (- get_) as key and the data as value.
        eg.
        get_username -> username: "miskibin"
        """
        data = {}
        for method in self.get_methods:
            data[str(method.split("get_")[1])] = getattr(self, method)()
        self.logger.debug(f"{data.keys()}")
        return data

    def get_win_ratio_per_color_conclusions(self) -> list[tuple]:
        """
        input data: [white_win, white_draws, white_lost, black_win, black_draws, black_lost]
        return: list of 3 conclusions
        """
        data = self.data["win_ratio_per_color"]["total"]
        data = data["black"] + data["white"]
        if data[0] - data[2] > data[3] - data[5]:
            first = (
                "You doing better as white. You should learn some openings from black side.",
                1,
            )
        else:
            first = (
                "You doing better as black. You should learn some openings from white side.",
                1,
            )
        if data[0] + data[3] < data[2] + data[5]:
            second = (
                "You are losing more games than winning. You are probably overrated.",
                0,
            )
        else:
            second = (
                "You are winning more games than losing. You are probably underrated.",
                1,
            )

        if data[1] + data[4] > 0.1 * sum(data):
            third = (
                "You are drawing too many games. Maybe try to play more aggressively.",
                0,
            )
        else:
            third = (
                "You are not drawing too many games. Keep it up. Your games are interesting.",
                1,
            )
        return [first, second, third]
