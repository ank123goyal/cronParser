import argparse
from cronParser import CronParser

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument(dest='minuteStr', help='[Mandatory] Please provide the minute')
	parser.add_argument(dest='hourStr', help='[Mandatory] Please provide the hour')
	parser.add_argument(dest='dayOfMonth', help='[Mandatory] Please provide the Day of Month')
	parser.add_argument(dest='month', help='[Mandatory] Please provide the Month')
	parser.add_argument(dest='dayOfWeek', help='[Mandatory] Please provide Day of the Week')
	parser.add_argument(dest='command', help='[Mandatory] Please provide the command')

	args = parser.parse_args()
	# Extract arguments
	print args

	minuteStr = args.minuteStr
	hourStr = args.hourStr
	dayOfMonth = args.dayOfMonth
	month = args.month
	dayOfWeek = args.dayOfWeek
	command = args.command

	# # Parse the cron expression and describe
	cronParser = CronParser(segments=[minuteStr, hourStr, dayOfMonth, month, dayOfWeek], command=command)
	cronParser.parse()

if __name__ == "__main__":
	main()


