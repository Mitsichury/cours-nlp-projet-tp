import logging
from botocore.vendored import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

URL = "http://54.246.250.50:5001/board"


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


def handle_play(event):
    ## ----- TODO : Build the application logic with the backend and answer to the user ----- ##
    cell = event['currentIntent']['slots']["Choice"]
    message = "You want to play " + str(cell)
    ## -------------------------------------------------------------------------------------- ##

    return {
        'sessionAttributes': event['sessionAttributes'],
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }
    }


def handle_restart(event):
    ## ----- TODO : Restart the game and answer to the user ----- ##
    return {
        'sessionAttributes': event['sessionAttributes'],
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'contentType': 'PlainText',
                'content': "Not done yet"
            }
        }
    }
    ## ---------------------------------------------------------- ##


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
    elif event['currentIntent']['name'] == "Retry":
        return handle_restart(event)
    else:
        return handle_default(event)
