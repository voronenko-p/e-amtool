from datetime import datetime, timedelta
from unittest import TestCase
from amtoolhelper import AmtoolHelper

ALERTMANAGER_HOST = "http://10.9.0.138:9093/api/v2"


class TestAmtoolHelper(TestCase):
    def test_get_status(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        amtoolhelper.get_status()

    def test_get_alerts(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        alerts = amtoolhelper.get_alerts()
        self.assertIsNotNone(alerts)

    def test_get_silences(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        silences = amtoolhelper.get_silences()
        self.assertIsNotNone(silences)

    def test_get_silence(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        silence = amtoolhelper.get_silence(silence_id="bb788860-35d2-48e7-9062-f082c77d202d")
        self.assertIsNotNone(silence)

    def test_post_silence(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        silence = amtoolhelper.post_silence(
            matchers=[{ "instance": "i-028ae8bf36be2e188"}],
            starts_at=datetime.now(),
            ends_at=datetime.now() + timedelta(hours=1),
            created_by="Someone",
            comment="test silence"
        )
        self.assertIsNotNone(silence)
