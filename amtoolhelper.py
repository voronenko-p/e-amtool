from __future__ import print_function
import time
import swagger_client
from swagger_client import Configuration, ApiClient
from swagger_client.rest import ApiException
from pprint import pprint


class AmtoolHelper(object):

    def __init__(self, alertmanager_address):
        self.configuration = Configuration()
        self.configuration.host = alertmanager_address
        api_client = ApiClient(configuration=self.configuration)
        self.api_instance = swagger_client.GeneralApi(api_client=api_client)

    def get_status(self):
        try:
            api_response = self.api_instance.get_status()
            return api_response
        except ApiException as e:
            print("Exception when calling GeneralApi->get_status: %s\n" % e)
        return {}        
