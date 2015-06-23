from sys import argv
from os import environ
from datetime import datetime, timedelta
import requests

from twilio.rest import TwilioRestClient


TWILIO_ID = environ.get('TWILIO_YANKEES_ID')
TWILIO_TOKEN = environ.get('TWILIO_YANKEES_TOKEN')
TWILIO_NUMBER = environ.get('TWILIO_YANKEES_NUMBER')


def get_game_url(game_date):
    baseball_url = "http://gd2.mlb.com/components/game/mlb/year_{year}/month_{month}/day_{day}/master_scoreboard.json".format(
        year=game_date.year,
        month=game_date.strftime("%m"),
        day=game_date.strftime("%d")
        )
    return baseball_url


def get_game_data(days_ago=1):
    """
    Add date argument at some point
    """
    game_date = datetime.now() - timedelta(days=days_ago)
    request_url = get_game_url(game_date)
    baseball_data = requests.get(request_url)
    game_data = baseball_data.json()
    game_array = game_data['data']['games']['game']
    return game_array


def find_winner(team, game_data):
    try:
        game_score = [{g['home_name_abbrev']:int(g['linescore']['r']['home']), g['away_name_abbrev']:int(g['linescore']['r']['away'])} for g in game_data if (team in g['home_name_abbrev'] or team in g['away_name_abbrev'])]

        runs_scored = game_score[0][team]
        if runs_scored is max(game_score[0].values()) and runs_scored >= 6:
            message = "Yankees won! Use YANKEES6 at www.papajohns.com for 50% off! :-)"
        else:
            message = "No luck today, Yankees lost."
    except Exception as e:
        message = e
    return message


def send_message(message, to_number):
    client = TwilioRestClient(TWILIO_ID, TWILIO_TOKEN)
    text_message = client.messages.create(
        body=message,
        to=to_number,
        from_=TWILIO_NUMBER
        )
    print(message)


if __name__ == '__main__':
    if len(argv) > 2:
        team_name = argv[1]
        game_data = get_game_data()
        winner = find_winner(team_name, game_data)
        to_number = argv[2]
        send_message(winner, to_number)
    else:
        raise Exception("You must pass an abbreviated team name and phone number as arguments")
