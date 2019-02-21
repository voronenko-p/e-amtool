from unittest import TestCase
from amtoolhelper import AmtoolHelper

ALERTMANAGER_HOST = "http://10.9.0.138:9093/api/v2"


class TestAmtoolHelper(TestCase):
    def test_get_status(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        amtoolhelper.get_status()

    def test_get_status(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        amtoolhelper.get_alerts()
