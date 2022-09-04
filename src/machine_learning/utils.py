import chessdotcom
#from tools.games_parser.Game import Game
from pprint import pprint

def get_curr_game(username):
    response = chessdotcom.get_player_current_games(username).json
    pprint(response['games'])
    
get_curr_game('Barabasz60')