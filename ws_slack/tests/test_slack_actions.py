import unittest
from unittest import TestCase
from .. import slack_actions


class TestSlackActions(TestCase):
    def test_fix_slack_channel_name(self):
        res = slack_actions.fix_slack_channel_name(channel_name="NAME .")
        self.assertEqual(res, "name__")


if __name__ == '__main__':
    unittest.main()
