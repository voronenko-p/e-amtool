import os
import re
from datetime import datetime
from errbot import arg_botcmd, botcmd, BotPlugin
from amtoolhelper import AmtoolHelper


def get_ts():
    now = datetime.now()
    return '%s.%d' % (now.strftime('%Y%m%d-%H%M%S'), now.microsecond)


class SaAmtool(BotPlugin):

    def get_configuration_template(self):
        return {'server_address': 'https://host:9093/api/v1'}

    @botcmd(template='amtool_status')
    def amtool_status(self, mess, args):
        """List of alerts"""
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'],
            alertmanager_token=self.config['token'])
        result = helper.get_alerts()
        return {'alerts': result}

