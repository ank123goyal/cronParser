import unittest
from cronParser import CronParser
from enums import ExpressionType

class TestCronParser(unittest.TestCase):

	def setUp(self):
		pass

	def test_minute_str(self):
		cronParse = CronParser(['*/15', "0", "1", "1", "1"], command="/user/func1.py")
		minuteStr = "*/15"
		minutes = cronParse.parseForType(minuteStr, ExpressionType.MINUTE)
		self.assertEqual(minutes, [0, 15, 30, 45])

	def test_hour_str(self):
		cronParse = CronParser(['*/15', "*/15", "1", "1", "1"], command="/user/func1.py")
		minuteStr = "*/3"
		minutes = cronParse.parseForType(minuteStr, ExpressionType.HOUR)
		self.assertEqual(minutes, [0, 3, 6, 9, 12, 15, 18, 21])

if __name__ == "__main__":
	unittest.main()