"""
Project: Data-Mining GOG (Good Old Games)
Game Scrapper File
"""
from Scripts.Scrapper.import_game_details import get_game_details
from Scripts.Scrapper.import_game_data import get_game_data
from bs4 import BeautifulSoup
import config


def game_page_scrapper(game_page_url):
    """
    Returns ALL the available data from the game's page url.
    :param game_page_url: Response object (requests library)
    :return: game_sql(dict) with all the game info.
    """
    soup = BeautifulSoup(game_page_url.content, features=config.BEAUTIFUL_SOUP_FEATURE)
    # Game data section
    game_data_dict = get_game_data(game_page_url, soup)

    # Game details section
    game_details_dict = get_game_details(soup)

    # Merging general data with game details section
    game_sql = {**game_data_dict, **game_details_dict}
    return game_sql
