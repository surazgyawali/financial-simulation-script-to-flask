import requests

import flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request

from game.app import app


def send_post_request():

    try:
        response = requests.post(
            flask.request.url_root + "api/game",
            headers={"sessid": getSessionId()},
        )
        jsonData = response.json()
        responseMessage = jsonData["data"]
        return responseMessage
    except requests.exceptions.RequestException as e:
        return
    except KeyError as e:
        """key error"""
        return
    except Exception as e:
        """uncatched exception"""
        return


def send_get_request(response):
    """returns gamedata when passed response"""
    headerData = {
            "sessid": getSessionId(),
            "message": response
        }
    try:
        response = requests.get(flask.request.url_root + "api/game", headers=headerData)
        jResponse = response.json()
        messages = jResponse["data"]
        return messages

    except requests.exceptions.RequestException as e:
        """ request exception"""
        return e
    except KeyError as e:
        """key error"""
        return
    except Exception as e:
        """uncatched exception"""
        return


def game_loop(header, messages=None):
    """renders gameloop view with provided header parameter"""
    return render_template(
        "game.djhtml",
        messages=messages,
        header=header,
        # sessid     = app.queue_in[app.queue],
        **gameLoopQuestions()
    )


def gameLoopQuestions():
    "returns game loop questions in json/dict format"
    return {
        "options": [
            "1:Hire/fire underwriters.",
            "2:Check platform income statement.",
            "3:Check platform balance sheet.",
            "4:Check platform cash flow statement.",
            "5:Check loan performance.",
            "6:Check loan buyer cash.",
            "7:Sell loans.",
            "8:Securitize loans.",
            "9:Sell into credit facility.",
            "10:Refinance credit facility.",
            "11:Credit facility info.",
            "12:Move to next quarter.",
            "13:Quit.",
        ],
        "question": "Make a decision",
        "uri": "/game",
        "field_name": "main",
    }


def validateResponse(response):
    if not response:
        return False
    return True


def getSessionId():
    sessionId = list(app.in_queue.keys())[-1] if app.in_queue else None
    print("\nsesid:",sessionId)
    return sessionId