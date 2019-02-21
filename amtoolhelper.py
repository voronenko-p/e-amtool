from __future__ import print_function
import time
import swagger_client
from swagger_client import Configuration, ApiClient, api
from swagger_client.rest import ApiException
from pprint import pprint


class AmtoolHelper(object):

  def __init__(self, alertmanager_address):
    self.configuration = Configuration()
    self.configuration.host = alertmanager_address
    api_client = ApiClient(configuration=self.configuration)
    self.general_api = swagger_client.GeneralApi(api_client=api_client)
    self.alerts_api = swagger_client.AlertApi(api_client=api_client)
    self.receiver_api = swagger_client.ReceiverApi(api_client=api_client)
    self.silence_api = swagger_client.SilenceApi(api_client=api_client)

  def get_status(self):
    try:
      api_response = self.general_api.get_status()
      return {
        "cluster": {
          "name": api_response.cluster.name,
          "status": api_response.cluster.status,
#          "peers": api_response.cluster.peers
        },
        "config": api_response.config.original,
        "uptime": api_response.uptime,
        "version": {
          "branch": api_response.version_info.branch,
          "build_date": api_response.version_info.build_date,
          "version": api_response.version_info.version,
          "revision": api_response.version_info.revision,

        }
      }
    except ApiException as e:
      print("Exception when calling GeneralApi->get_status: %s\n" % e)
    return {}

  #        active = true # bool | Show active alerts (optional) (default to true)
  #        silenced = true # bool | Show silenced alerts (optional) (default to true)
  #        inhibited = true # bool | Show inhibited alerts (optional) (default to true)
  #        unprocessed = true # bool | Show unprocessed alerts (optional) (default to true)
  #        filter = ['filter_example'] # list[str] | A list of matchers to filter alerts by (optional)
  #        receiver = 'receiver_example' # str | A regex matching receivers to filter alerts by (optional)
  def get_alerts(self, active=True, silenced=True, inhibited=True,
      unprocessed=True, filter=[], receiver=""):
    try:
      api_response = self.alerts_api.get_alerts(active=active,
                                                  silenced=silenced,
                                                  inhibited=inhibited,
                                                  unprocessed=unprocessed,
                                                  filter=filter,
                                                  receiver=receiver
                                                )
      return {
          "count": len(api_response),
          "alerts": api_response,
          "criteria": {
              "active": active,
              "silenced": silenced,
              "inhibited": inhibited,
              "unprocessed": unprocessed,
              "filter": filter,
              "receiver": receiver
          }
      }
    except ApiException as e:
      print("Exception when calling AlertApi->get_alerts: %s\n" % e)
    return {}
