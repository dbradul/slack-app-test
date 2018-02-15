import json
import requests
import flask
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random
import math
import sys
import traceback
import re
import resources
import demo


from pprint import pprint as pp
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, make_response
from imgurpython import ImgurClient

SLACK_BOT_TOKEN     = os.environ.get('SLACK_BOT_TOKEN')
SLACK_WEBHOOK_INC   = os.environ.get('SLACK_WEBHOOK_INC')
SLACK_VERIFICATION_TOKEN = os.environ.get('SLACK_VERIFICATION_TOKEN')

IMGUR_CLIENT_ID     = os.environ.get('IMGUR_CLIENT_ID')
IMGUR_CLIENT_SECRET = os.environ.get('IMGUR_CLIENT_SECRET')

#------------------------------------------------------------------------------
app = Flask(__name__)
executor = ThreadPoolExecutor(1)


#------------------------------------------------------------------------------
@app.route('/', methods=['GET'])
def on_root():
    return make_response('<h1>Hello world!</h1>', 200)


#------------------------------------------------------------------------------
@app.route('/api/v1/interactive_action', methods=['POST'])
@demo.debug_request(request='json.loads(flask.request.values["payload"])')
def on_interactive_action():

    response_text = ''
    interactive_action = json.loads(flask.request.values["payload"])

    try:

        if interactive_action["type"] == "interactive_message":
            pass

        elif interactive_action["type"] == "dialog_submission":

            #TODO: input validation
            executor.submit(
                build_plot,
                interactive_action
            )

    except Exception as ex:
        response_text = ":x: Error: `%s`" % ex

    return make_response(response_text, 200)



# ----------------------------------------------------------------------------------------------------------------
def upload_to_imgur(filepath):
    client = ImgurClient(IMGUR_CLIENT_ID,
                         IMGUR_CLIENT_SECRET)

    response = client.upload_from_path(filepath)

    # pp("Response from 'ImgurClient': %s" % response)

    return response['link']


#------------------------------------------------------------------------------
@app.route('/api/v1/btc', methods=['POST'])
@demo.debug_request(request='flask.request.values')
def on_btc():

    response = requests.get(
        url='https://api.coindesk.com/v1/bpi/currentprice.json',
    )

    resp_obj = json.loads(response.text)
    pp(resp_obj)

    request = flask.request.values

    demo.slack_send_response(
        text=':us:: %s' % resp_obj['bpi']['USD']['rate'],
        url=request['response_url'],
        icon=':chart_with_upwards_trend:'
    )

    # return make_response(':us:: %s' % resp_obj['bpi']['USD']['rate'], 200)
    return make_response('', 200)


#------------------------------------------------------------------------------
@app.route('/api/v1/plot', methods=['POST'])
@demo.debug_request(request='flask.request.values')
def on_plot():

    data = {
        "token": SLACK_BOT_TOKEN,
        'trigger_id': flask.request.values["trigger_id"],
        "dialog": json.dumps(resources.dialog_plot)
    }

    response = requests.post(
        url="https://slack.com/api/dialog.open",
        data=data
    )

    pp(response)

    return make_response("Processing started...", 200)


#-------------------------------------------------------------------------
def build_plot(message):

    pp('Task started...')

    try:
        tmp_filepath = '/tmp/%s.png' % random.randint(1e6, 1e7)

        submission = message['submission']
        formula = submission['formula']
        range_start = float(submission['x_from'])
        range_stop = float(submission['x_to'])
        step  = float(submission['step'])
        colour = submission['colour'][:1]
        formula_replaced = formula.replace('x', '__')

        x_value = []
        while (range_start <= range_stop):
            x_value.append(range_start)
            range_start += step

        y_value = [eval(formula_replaced) for __ in x_value]

        plt.ioff()
        plt.clf()
        plt.plot(x_value, y_value, colour)
        plt.savefig(tmp_filepath)
        url = upload_to_imgur(tmp_filepath)

        attachments = [{
            "text" : '`y=%s`' % formula,
            "image_url" : url
        }]

        response_text = ':v:'

    except Exception as ex:
        response_text = ':x: Что-то пошло не так: `%s`' % ex
        attachments = None

    demo.slack_send_webhook(
        text=response_text,
        channel=message['channel']['id'],
        icon=':chart_with_upwards_trend:',
        attachments=attachments
    )


#------------------------------------------------------------------------------
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, threaded=True)
