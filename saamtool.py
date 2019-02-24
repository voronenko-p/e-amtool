import os
import re
from datetime import datetime, timedelta
from errbot import arg_botcmd, botcmd, BotPlugin
from amtoolhelper import AmtoolHelper
import parsedatetime as pdt# $ pip install parsedatetime

def get_ts():
    now = datetime.now()
    return '%s.%d' % (now.strftime('%Y%m%d-%H%M%S'), now.microsecond)


class SaAmtool(BotPlugin):

    def get_configuration_template(self):
        return {
            'server_address': 'https://host:9093/api/v2',
            'time_zone': 'Europe/Kiev'
        }

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
        return {"silences": result}

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

    @arg_botcmd('--weeks', type=int, default=0)
    @arg_botcmd('--days', type=int, default=0)
    @arg_botcmd('--hours', type=int, default=0)
    @arg_botcmd('--minutes', type=int, default=0)
    @arg_botcmd('fingerprint', type=str,template='amtool_silence_add')
    def amtool_suppress(self, mess, fingerprint, weeks, days, hours, minutes):
        """Puts exact suppress match on alert"""
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])

        start_period = datetime.now().utcnow()
        end_period = start_period + timedelta(minutes=minutes, hours=hours, days=days, weeks=weeks)

        alert = helper.get_alert(fingerprint)
        matchers = helper.get_matchers_by_alert(alert)

        result = helper.post_silence(
            matchers=matchers,
            starts_at=start_period.isoformat(),
            ends_at=end_period.isoformat(),
            created_by="errbot",
            comment="errbot"
        )
        return result

        # Amtool compability aliases

    @arg_botcmd('--inhibited', dest='inhibited', type=bool, default=True)
    @arg_botcmd('--silenced', dest='silenced', type=bool, default=True)
    @arg_botcmd('--active', dest='active', type=bool, default=True)
    @arg_botcmd('--unprocessed', dest='unprocessed', type=bool, default=True)
    @arg_botcmd('--receiver', dest='receiver', type=str, default="")
    @arg_botcmd('matchers', type=str, template='amtool_alert_query')
    def amtool_alert_query(self, inhibited, silenced, active, unprocessed, receiver, matchers):
        """
          Queries alert in amtool command style
          --inhibited          Show inhibited alerts
          --silenced           Show silenced alerts
          --active             Show active alerts
          --unprocessed        Show unprocessed alerts
          --receiver=RECEIVER  Show alerts matching receiver (Supports regex syntax)

        Args:
          [<matcher-groups>]  Query filter
        """

        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.get_alerts(
            active=active,
            silenced=silenced,
            inhibited=inhibited,
            unprocessed=unprocessed,
            filter=[],
            receiver=receiver
        )
        return result

    @arg_botcmd('--author', type=str, default=None)
    @arg_botcmd('--duration', type=str, default="1 minute")
    @arg_botcmd('--start', type=str, default=None)
    @arg_botcmd('--end', type=str, default=None)
    @arg_botcmd('--comment', type=str, default=None)
    @arg_botcmd('matchers', type=str,template='amtool_silence_add')
    def amtool_silence_add(self, mess, author, duration, start, end, comment, matchers):
        """
            usage: !amtool silence add [<flags>] [<matcher-groups>...]

            Add a new alertmanager silence

                Amtool uses a simplified Prometheus syntax to represent silences. The
                non-option section of arguments constructs a list of "Matcher Groups"
                that will be used to create a number of silences. The following examples
                will attempt to show this behaviour in action:

                !amtool silence add alertname=foo node=bar

                    This statement will add a silence that matches alerts with the
                    alertname=foo and node=bar label value pairs set.

                !amtool silence add foo node=bar

                    If alertname is omitted and the first argument does not contain a '=' or a
                    '=~' then it will be assumed to be the value of the alertname pair.

                !amtool silence add 'alertname=~foo.*'

                    As well as direct equality, regex matching is also supported. The '=~' syntax
                    (similar to Prometheus) is used to represent a regex match. Regex matching
                    can be used in combination with a direct match.

              --author="slavko"  Username for CreatedBy field
              --duration="1h"    Duration of silence
              --start=START      Set when the silence should start. RFC3339 format 2006-01-02T15:04:05-07:00
              --end=END          Set when the silence should end (overwrites duration). RFC3339 format 2006-01-02T15:04:05-07:00
              --comment=COMMENT  A comment to help describe the silence

        """
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        if start is not None:
            start_period = datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')
        else:
            start_period = datetime.now().utcnow()

        if end is not None:
            end_period = datetime.strptime(end, '%Y-%m-%dT%H:%M:%SZ')
        else:
            cal = pdt.Calendar()
            diff = cal.parseDT(duration, sourceTime=datetime.min)[0] - datetime.min
            end_period = start_period + diff

        result = helper.post_silence(
            matchers=matchers,
            starts_at=start_period.isoformat(),
            ends_at=end_period.isoformat(),
            created_by=author,
            comment=comment
        )
        return result

    @arg_botcmd('silence_id', type=str)
    def amtool_silence_expire(self, mess, silence_id):
        """
             amtool silence expire silence-id

            expire an alertmanager silence

            Args:
              silence-id  Id of silences to expire
        """
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.delete_silence(silence_id)
        return result

    @arg_botcmd('--expired', type=bool, default=None)
    @arg_botcmd('--within', type=str, default=None, template="amtool_silence_query")
    def amtool_silences(self, mess, args):
        """
          Amtool has a simplified prometheus query syntax The non-option section of arguments constructs a list of "Matcher Groups"
          that will be used to filter your query. The following examples will attempt to show this behaviour in action:

          amtool silence query alertname=foo node=bar

          This query will match all silences with the alertname=foo and node=bar label
          value pairs set.

          amtool silence query foo node=bar

          If alertname is omitted and the first argument does not contain a '=' or a
          '=~' then it will be assumed to be the value of the alertname pair.

          amtool silence query 'alertname=~foo.*'

          As well as direct equality, regex matching is also supported. The '=~' syntax
          (similar to prometheus) is used to represent a regex match. Regex matching
          can be used in combination with a direct match.

          In addition to filtering by silence labels, one can also query for silences that are due to expire soon
          with the "--within" parameter. In the event that you want to preemptively act upon expiring silences by
          either fixing them or extending them. For example:

          amtool silence query --within 8h

          returns all the silences due to expire within the next 8 hours. This syntax can also be combined with the label based
          filtering above for more flexibility.

          The "--expired" parameter returns only expired silences. Used in combination with "--within=TIME", amtool returns
          the silences that expired within the preceding duration.

          amtool silence query --within 2h --expired

returns all silences that expired within the preceeding 2 hours.

      --expired        Show expired silences instead of active
      --within=WITHIN  Show silences that will expire or have expired within a duration
        """
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.get_silences()
        return {"silences": result}
