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
        return {'server_address': 'https://host:9093/api/v2'}

    @botcmd(template='amtool_status')
    def amtool_status(self, mess, args):
        """Returns alert manager status"""
        self.log.info("Current config {0}".format(self.config))
        self.log.info(
            "Alertmanager @ {0}".format(self.config['server_address']))
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.get_status()
        return result

    @botcmd(template='amtool_alerts')
    def amtool_alerts(self, mess, args):
        """Returns current alerts list"""
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.get_alerts()
        return result

    @botcmd(template='amtool_alerts_brief')
    def amtool_brief(self, mess, args):
        """Returns brief on alerts"""
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.get_alerts()
        return result
