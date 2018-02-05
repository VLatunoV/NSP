class Shift:
	def __init__(self):
		self.name = ''
		self.length = 0
		self.prohibitNext = set()


class StaffMember:
	def __init__(self):
		self.name = ''
		self.maxShifts = dict()
		self.maxTotalMinutes = 0
		self.minTotalMinutes = 0
		self.maxConsecutiveShifts = 0
		self.minConsecutiveShifts = 0
		self.minConsecutiveDaysOff = 0
		self.maxWeekends = 0

class ProblemInstance:
	'''
	Every problem starts on a Monday at index 0
	'''

	def __init__(self):
		self.numberOfDays = 0
		self.shifts = dict()
