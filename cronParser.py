from enums import ExpressionType
from datetime import datetime
from calendar import monthrange
import re

_cronMonths = {
	1: 'JAN',
	2: 'FEB',
	3: 'MAR',
	4: 'APR',
	5: 'MAY',
	6: 'JUN',
	7: 'JUL',
	8: 'AUG',
	9: 'SEP',
	10: 'OCT',
	11: 'NOV',
	12: 'DEC'
}

_cronDays = {
	0: 'SUN',
	1: 'MON',
	2: 'TUE',
	3: 'WED',
	4: 'THU',
	5: 'FRI',
	6: 'SAT'
}


class CronParser:

	def __init__(self, segments, command):
		self.segments = segments
		self.command = command

	def parse(self):
		minuteStr = self.segments[0]
		hourStr = self.segments[1]
		daysOfMonthStr = self.segments[2]
		monthStr = self.preProcessSegment(self.segments[3], _cronMonths) # Preprocess to handle JAN-DEC
		dayOfWeekStr = self.preProcessSegment(self.segments[4], _cronDays)
		command = self.command

		self.validateExpression([minuteStr, hourStr, daysOfMonthStr, monthStr, dayOfWeekStr])

		minutes = self.parseForType(minuteStr, ExpressionType.MINUTE)
		hours = self.parseForType(hourStr, ExpressionType.HOUR)
		months = self.parseForType(monthStr, ExpressionType.MONTH) # TODO: Handle L,W
		daysOfMonth = self.parseForType(daysOfMonthStr, ExpressionType.DAY_OF_MONTH)
		dayOfWeek = self.parseForType(dayOfWeekStr, ExpressionType.DAY_OF_WEEK)


		self.describeCron(minutes, hours, daysOfMonth, months, dayOfWeek, command)

	def preProcessSegment(self, segmentStr, dataDict):
		for key in dataDict:
			segmentStr = segmentStr.upper().replace(dataDict[key], str(key))
		return segmentStr

	def describeCron(self, minutes, hours, daysOfMonth, months, dayOfWeek, command):

		print "Minutes:", sorted(set(minutes))
		print "Hours:", sorted(set(hours))
		print "daysOfMonth:", sorted(set(daysOfMonth))
		print "Months:", sorted(set(months))
		print "Day of week:", sorted(set(dayOfWeek))
		print "Command: ", command

	def validateExpression(self, segments):
		if len(segments) != 5:
			raise Exception("Invalid Segments")

		pattern = re.compile('/(\d+,)+\d+|(\d+(\/|-)\d+)|\d+|\*/')
		for segment in segments:
			if segment != "*" and not pattern.match(segment):
				raise Exception("Parsing Error")

	def parseDayOfMonth(self, expressionStr, month):
		# W - nearest weekday of the month
		# L is last day
		# TODO: handle year - currently handly current year
		now = datetime.now() #
		year = now.year
		start, end = monthrange(year, month)

		return self.parseExpression(expressionStr, [i for i in xrange(start, end+1)])

	def parseForType(self, expressionStr, type):

		parserFunc = {
			ExpressionType.MINUTE: self.parseExpression(expressionStr, [i for i in xrange(0, 60)]),
			ExpressionType.HOUR: self.parseExpression(expressionStr, [i for i in xrange(0, 24)]),
			ExpressionType.MONTH: self.parseExpression(expressionStr, [i for i in xrange(1, 13)]),
			ExpressionType.DAY_OF_MONTH: self.parseExpression(expressionStr, [i for i in xrange(1, 32)]),
			ExpressionType.DAY_OF_WEEK: self.parseExpression(expressionStr, [i for i in xrange(0, 7)])
		}
		return parserFunc[type]


	def parseExpression(self, expressionStr, allValues):
		# , - * /
		# 0-59
		# 0,1,2
		# */3, all divisible by 3
		# 2/3, 2, 5, 8, ...
		if expressionStr == "*":
			return allValues  # [i for i in xrange(60)]
		elif any(val in expressionStr for val in ['/', '-', ',']) is False:
			return [int(expressionStr)]  # TODO: check if ints in valid range
		elif "," in expressionStr:
			segments = expressionStr.split(",")  # 1,2 # 1,2-3 # 1,* # 1,4-5/2
			values = []
			# 1,2 # 1,2-3 # 1,* # 1,4-5/2
			for segment in segments:
				values.extend(self.parseExpression(segment, allValues))

			return values

		elif "/" in expressionStr:  # handle / or (-)
			segments = expressionStr.split("/")  # 1/3 or 1-4/3
			segment1 = segments[0]  # 1 or 1-4
			segment2 = segments[1]  # /3

			if "-" in segment1:
				start, end = segment1.split("-")  # 1-4
				delta = int(segment2)  # 4/3 - delta= 3
				values = self.__generateRange(int(start), int(end), delta, allValues)

				return values
			elif segment1 == "*":  # */3
				start = 0
				last = allValues[-1]
				delta = int(segment2)  # 4/3 - delta= 3
				values = self.__generateRange(int(start), last, delta, allValues)
				return values

			else:  # 4/3
				start = int(segment1)
				last = allValues[-1]
				delta = int(segment2)  # 4/3 - delta= 3
				values = self.__generateRange(int(start), last, delta, allValues)
				return values
		elif "-" in expressionStr:
			start, end = expressionStr.split("-")
			# error case if last > range
			start = max(int(start), allValues[0])
			last = min(int(end), allValues[-1])

			values = self.__generateRange(int(start), last, 1, allValues)
			return values

		return []

	def __generateRange(self, start, end, delta, allValues):
		values = []
		# TODO: error case if last > range or start < range
		start = max(start, allValues[0])
		last = min(end, allValues[-1])
		for val in xrange(start, last + 1, delta):
			values.append(val)

		return values
