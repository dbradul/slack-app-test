import time

from slackclient import SlackClient


class ChatBot:

    # -------------------------------------------------------------------------
    def __init__(self, slack_bot_token, read_websocket_delay_sec):
        self._slack_client = SlackClient(slack_bot_token)
        self._users = []
        self._read_websocket_delay_sec = read_websocket_delay_sec


    # -------------------------------------------------------------------------
    def _fetch_users(self):
        api_call = self._slack_client.api_call("users.list")
        if api_call.get('ok'):
            self._users = api_call.get('members')

    # -------------------------------------------------------------------------
    def get_user_by_id(self, user_id):
        for user in self._users:
            if user['id'] == user_id:
                return user
        return {}

    # -------------------------------------------------------------------------
    def _parse_slack_message(self, slack_rtm_msg):
        if slack_rtm_msg:
            for event in slack_rtm_msg:
                if event.get('type') == 'message':
                    channel = event.get('channel')
                    user = event.get('user')
                    text = event.get('text')

                    return text, channel, user

        return None, None, None


    # ----------------------------------------------------------------------------------------------------------------
    def _handle_command(self, text, channel, user_id):

        if not self.get_user_by_id(user_id).get('is_bot'):#user_id != SLACK_BOT_UID:

            user_name = self.get_user_by_id(user_id).get('name')

            if text.lower().startswith('hello'):
                reply = 'Hi, %s' % user_name
            elif text.lower().startswith('bye'):
                reply = 'Bye, %s' % user_name
            else:
                reply = 'Unknown greeting :('

            self._slack_client.api_call(
                method="chat.postMessage",
                channel=channel,
                as_user=True,
                text=reply
            )


    # ----------------------------------------------------------------------------------------------------------------
    def run(self):

        if self._slack_client.rtm_connect():
            print("StarterBot connected and running!")
            self._fetch_users()

            while True:
                inc_msg = self._slack_client.rtm_read()
                print(inc_msg)

                text, channel, user = self._parse_slack_message(inc_msg)

                if text and channel and user:
                    self._handle_command(text, channel, user)

                time.sleep(self._read_websocket_delay_sec)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
