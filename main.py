"""
Project: Data-Mining GOG (Good Old Games)u
Creator: Roy Toledano
Main File - Please run this file to start the script
"""

from Scripts.DB import db_creator
import config as cf
from Scripts.Scrapper.main_scrapper import game_page_scrapper
from Scripts.Scrapper.selenium_get_all_games_URLs import get_game_urls
from Scripts.DB.mysql_writer import WebsiteDB
from Scripts import cli_cmd_parser
from Scripts.import_Twitch_popularity_API import ApiTwitch
import grequests
from datetime import datetime


if __name__ == '__main__':
    n_is_test = True #todo: delete, just to QA to db creation without handling the error of the old script.
    print("""
            ***********************************
            Good Old Games Scrapper has Started
            ***********************************
            """)
    list_of_games_dict = []  # list of all batches into mysql_data_mining
    gog_url_partial, args = cli_cmd_parser.filter_args()

    # Twitch API
    if (not n_is_test) and args.twitch == "yes":
        api = ApiTwitch()
        call = api.api_twitch_to_mysql()

    # MySQL Create DB
    if args.db == 'yes':  # creates the database schema if -d was chosen yes
        db_creator.create_mysql_db()

    url_batch = []  # list of urls for grequests
    counter = 0

    # collecting all games urls and run all over it.
    for game_page in get_game_urls(gog_url_partial):
        print(f"game counter {counter}")
        counter += 1
        url_batch.append(game_page)

        # in every batch of collected games-> writes into DB.
        if len(url_batch) == cf.BATCH_SIZE:
            print("Batch Size is Full, writing to DB")
            responses = (grequests.get(link) for link in url_batch)
            # Game Scrapper
            # Iterates over the URLs
            for response in grequests.map(responses):
                try:
                    game_data = game_page_scrapper(response)

                    # print to screen results
                    if args.choice == 'screen' or args.choice == 'both':
                        print(game_data)

                    list_of_games_dict.append(game_data)
                except Exception as ex_message:
                    print("Issue 1", ex_message)

            # Write games details to DB
            if args.choice == 'db' or args.choice == 'both':
                try:
                    with WebsiteDB(list_of_games_dict) as db:
                        db.write_game_titles()
                        db.write_game_genres()
                        db.write_game_prices()
                        db.write_game_scores()
                except Exception as ex_message:
                    print(ex_message)

            list_of_games_dict.clear()
            url_batch.clear()

    if not n_is_test:
        sms_resp = sendSMS(f"Finished SCRAPPING GOG AT {datetime.now()}")
        print(sms_resp)
