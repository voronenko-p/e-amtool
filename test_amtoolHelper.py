from unittest import TestCase
from amtoolhelper import AmtoolHelper

ALERTMANAGER_HOST = "http://10.9.0.138:9093/api/v1"


class TestAmtoolHelper(TestCase):
  def test_get_status(self):
    amtoolhelper = AmtoolHelper(alertmanager_host=ALERTMANAGER_HOST)
    amtoolhelper.get_status()
