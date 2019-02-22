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

    @botcmd(template='amtool_silences')
    def amtool_silences(self, mess, args):
        """Returns current silences list"""
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.get_silences()
        return result

    @botcmd(template='amtool_recievers')
    def amtool_silences(self, mess, args):
        """Returns current receivers list"""
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.get_receivers()
        return result

    @botcmd(template='amtool_alerts_brief')
    def amtool_brief(self, mess, args):
        """Returns brief on alerts"""
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.get_alerts()
        return result

    @botcmd(template='amtool_silence_add')
    def amtool_post_silence(self, mess, args):
        """Returns brief on alerts"""
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.post_silence(
            matchers=None,
            starts_at=None,
            ends_at=None,
            created_by=None,
            comment=None
        )
        return result
