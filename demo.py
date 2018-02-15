import requests
import os
import time
import json
import flask
import resources
import functools

from pprint import pprint as pp
from flask import Flask, make_response
from echo_bot import EchoBot



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



#
# #------------------------------------------------------------------------------
# @app.route('/api/v1/btc_v3', methods=['POST'])
# @debug_request(request='flask.request.values')
# def on_btc_v3():
#
#     # request_data = flask.request.values
#     # _debug_request(on_btc.__name__, request_data)
#
#     data_payload = {
#         'token': SLACK_BOT_TOKEN,
#         'trigger_id': flask.request.values['trigger_id'],
#         # 'channel': request_data['user_id'],
#         'text': 'What currency would you like to choose?',
#         'attachments': resources.attachment_currency_dialog
#     }
#
#     return make_response(
#         json.dumps(data_payload),
#         200,
#         {"Content-Type": "application/json"}
#     )


# #------------------------------------------------------------------------------
# @app.route('/api/v1/interactive_action', methods=['POST'])
# @debug_request(request='json.loads(flask.request.values["payload"])')
# def on_interactive_action():
#
#     interactive_action = json.loads(flask.request.values["payload"])
#     #_debug_request(on_interactive_action.__name__, interactive_action)
#
#     try:
#
#         if interactive_action["type"] == "interactive_message":
#
#             currency = interactive_action['actions'][0]['value']
#             response = requests.get(
#                 url='https://api.coindesk.com/v1/bpi/currentprice.json',
#             )
#             resp_obj = json.loads(response.text)
#             pp(resp_obj)
#
#             # slack_post_msg(
#             #     text=':flag-%s:: %s' % (currency[:2], resp_obj['bpi'][currency]['rate']),
#             #     channel=interactive_action["channel"]["id"],
#             #     icon=':chart_with_upwards_trend:',
#             #     ts=interactive_action['message_ts']
#             # )
#
#             slack_send_response(
#                 text=':flag-%s:: %s' % (currency[:2], resp_obj['bpi'][currency]['rate']),
#                 url=interactive_action['response_url'],
#                 icon=':chart_with_upwards_trend:',
#                 channel=interactive_action["channel"]["id"],
#             )
#
#         elif interactive_action["type"] == "dialog_submission":
#             pass
#
#         response_text = ''
#
#     except Exception as ex:
#         response_text = ":x: Error: `%s`" % ex
#
#     return make_response(response_text, 200)
#


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

    # echo_bot = EchoBot(
    #     slack_bot_token=SLACK_BOT_TOKEN,
    #     read_websocket_delay_sec=0.3
    # )
    # echo_bot.run()


# ----------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
