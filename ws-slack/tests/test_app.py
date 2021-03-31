import sys
from unittest import TestCase
import unittest
#sys.path.insert(0, '../')
from ws_sdk.web import WS
import ws_sdk.constants as constants
sys.path.append('../')

import app


class TestApp(TestCase):
    def setUp(self):
        self.ws = WS(url="WS_API_URL", user_key="USER_KEY", token="ORG_TOKEN", token_type=constants.ORGANIZATION)

    def test_hello(self):
        res = app.hello()

        self.assertEqual(res, "HOW TO USE THIS!")


if __name__ == '__main__':
    unittest.main()
