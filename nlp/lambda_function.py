import logging
import random

from botocore.vendored import requests
import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

URL = "http://ec2-63-33-198-73.eu-west-1.compute.amazonaws.com:5001/board"


def cell_slot_to_number(cell_slot):
    row, column = 1, 1  # Default is middle

    if 'top' in cell_slot:
        row = 0
    elif 'bottom' in cell_slot:
        row = 2

    if 'left' in cell_slot:
        column = 0
    elif 'right' in cell_slot:
        column = 2

    cell_number = row * 3 + column
    return cell_number


def cell_number_to_slot(cell_number):
    slots = [
        "top-left", "top", "top-right",
        "left", "middle", "right",
        "bottom-left", "bottom", "bottom-right"
    ]
    return slots[cell_number]


def format_map(map):
    str_map = ""
    i = 0
    while i < len(map):
        if i % 3 == 0:
            str_map += "<br>"
        str_map += str(map[i])
        i += 1
    return str_map


def handle_play(event):
    ## ----- TODO : Build the application logic with the backend and answer to the user ----- ##
    cell = event['currentIntent']['slots']["Choice"]
    cell_index = cell_slot_to_number(cell)
    data = {"move": cell_index}
    result = requests.put(URL, data=data)
    message = "You want to play " + str(cell_index)
    if result.status_code == 400:
        message += "\n" + str(result.json()["message"])
    else:
        message += "\nCarte:" + format_map(result.json()["board"])
        message += "\nplayer_move:" + str(result.json()["player_move"])
        message += "\ncomputer_move:" + str(result.json()["computer_move"])
        message += "\nwinner:" + str(result.json()["winner"])
    ## -------------------------------------------------------------------------------------- ##

    return {
        'sessionAttributes': event['sessionAttributes'],
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'contentType': 'PlainText',
                'content': "Message:" + message
            }
        }
    }


def handle_restart(event):
    requests.delete(URL)
    return {
        'sessionAttributes': event['sessionAttributes'],
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'contentType': 'PlainText',
                'content': "Done"
            }
        }
    }


def handle_default(event):
    return {
        'sessionAttributes': event['sessionAttributes'],
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'contentType': 'PlainText',
                'content': "Choix par défaut y a qwack dans la marre mon carnard "
            }
        }
    }


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    logger.debug('userId={}'.format(event['userId']))
    logger.debug('intentName={}'.format(event['currentIntent']['name']))
    logger.debug(event)

    if event['currentIntent']['name'] == "inquire_choice":
        return handle_play(event)
    elif event['currentIntent']['name'] == "restart_game":
        return handle_restart(event)
    else:
        return handle_default(event)
