import os
import re
from datetime import datetime, timedelta
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

    @arg_botcmd('silence_id', type=str,template='amtool_silence_details')
    def amtool_silence(self, mess, silence_id):
        """Returns specific silence details"""
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.get_silence()
        return result

    @botcmd(template='amtool_recievers')
    def amtool_receivers(self, mess, args):
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

    @arg_botcmd('weeks', type=int, default=0)
    @arg_botcmd('days', type=int, default=0)
    @arg_botcmd('hours', type=int, default=0)
    @arg_botcmd('minutes', type=int, default=0)
    @arg_botcmd('fingerprint', type=str,template='amtool_silence_add')
    def amtool_suppress(self, mess, fingerprint, weeks, days, hours, minutes):
        """Puts exact suppress match on alert"""
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])

        start_period = datetime.now()
        end_period = start_period + timedelta(minutes=minutes, hours=hours, days=days, weeks=weeks)

        alert = helper.get_alert(fingerprint)
        matchers = helper.get_matchers_by_alert(alert)

        result = helper.post_silence(
            matchers=matchers,
            starts_at=start_period,
            ends_at=end_period,
            created_by="errbot",
            comment="errbot"
        )
        return result
