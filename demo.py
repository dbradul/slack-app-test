import requests
import os
import time
import json
import flask
import resources
import functools

from pprint import pprint as pp
from flask import Flask, make_response
from chat_bot import ChatBot



# ----------------------------------------------------------------------------------------------------------------
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_WEBHOOK_INC = os.environ.get('SLACK_WEBHOOK_INC')
SLACK_VERIFICATION_TOKEN = os.environ.get('SLACK_VERIFICATION_TOKEN')

IMGUR_CLIENT_ID = os.environ.get('IMGUR_CLIENT_ID')
IMGUR_CLIENT_SECRET = os.environ.get('IMGUR_CLIENT_SECRET')

# ----------------------------------------------------------------------------------------------------------------
app = Flask(__name__)



# ----------------------------------------------------------------------------------------------------------------
def demo_slack_test():
    response = requests.post("https://slack.com/api/api.test")
    pp("response from slack [%d]: %s" % (
        response.status_code,
        response.text
    ))


# -----------------------------------------------------------------------------
def slack_send_webhook(text, channel, **kwargs):

    data = {
        "channel": channel,
        "text": text
    }

    data.update(kwargs)

    response = requests.post(
        url=SLACK_WEBHOOK_INC,
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    pp("response from 'send_webhook' [%d]: %s" % (
        response.status_code,
        response.text
    ))


# -----------------------------------------------------------------------------
def slack_send_response(text, url, **kwargs):

    data = {
        "response_type": "in_channel",
        "text": text
    }

    data.update(kwargs)

    response = requests.post(
        url=url,
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    pp("response from 'slack_send_response' [%d]: %s" % (
        response.status_code,
        response.text
    ))


#------------------------------------------------------------------------------
@app.route('/api/v1/btc', methods=['POST'])
def on_btc():

    response = requests.get(
        url='https://api.coindesk.com/v1/bpi/currentprice.json',
    )

    resp_obj = json.loads(response.text)
    pp(resp_obj)

    request = flask.request.values

    slack_send_response(
        text=':us:: %s' % resp_obj['bpi']['USD']['rate'],
        url=request['response_url'],
        icon=':chart_with_upwards_trend:'
    )

    # return make_response(':us:: %s' % resp_obj['bpi']['USD']['rate'], 200)
    return make_response('', 200)

# ----------------------------------------------------------------------------------------------------------------
def slack_post_msg(text, channel, **kwargs):
    data = {
        "token": SLACK_BOT_TOKEN,
        "channel": channel,
        "text": text
    }

    data.update(kwargs)

    response = requests.post(
        url="https://slack.com/api/chat.postMessage",
        data=data
    )

    pp("response from 'slack_post_msg' [%d]: %s" % (
            response.status_code,
            json.dumps(json.loads(response.text), indent=4)
    ))


#------------------------------------------------------------------------------
def debug_request(request):

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('-------------------')
            print('%s:' % func.__name__)
            print('-------------------')
            pp(eval(request), indent=8)
            print('\n\n')
            return func(*args, **kw)

        return wrapper

    return decorator


# ----------------------------------------------------------------------------------------------------------------
def demo_slack_incoming_msg_handler():

    app.run(host='0.0.0.0', port=8080, threaded=True)


# ----------------------------------------------------------------------------------------------------------------
def main():

    # demo_slack_test()

    # slack_send_webhook(
    #     text='Hello from epic bot!',
    #     #channel='#general',
    #     channel='#random', #"#random"
    #     icon_emoji=':sunglasses:'
    # )

    # slack_post_msg(
    #     text='Hello from epic bot!',
    #     channel='#general',
    #     #channel='#random',
    #     icon_emoji=':sunglasses:'
    # )

    demo_slack_incoming_msg_handler()

    # chat_bot = ChatBot(
    #     slack_bot_token=SLACK_BOT_TOKEN,
    #     read_websocket_delay_sec=0.3
    # )
    # chat_bot.run()


# ----------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
