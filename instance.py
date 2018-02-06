class Shift:
	def __init__(self):
		self.id = ''
		self.length = 0
		self.prohibitNext = set()

class StaffMember:
	'''
	maxShifts = {shiftID: maxCount}, ommited shifts are unconstrained
	maxWeekends = Maximum working weekends allowed
	'''
	def __init__(self):
		self.id = ''
		self.maxShifts = dict()
		self.maxTotalMinutes = 0
		self.minTotalMinutes = 0
		self.maxConsecutiveShifts = 0
		self.minConsecutiveShifts = 0
		self.minConsecutiveDaysOff = 0
		self.maxWeekends = 0

class Cover:
	def __init__(self):
		self.day = 0
		self.shiftId = ''
		self.requirement =  0
		self.weightForUnder = 0
		self.weightForOver = 0

class ProblemInstance:
	'''
	Every problem starts on a Monday at index 0
	'''
	def __init__(self):
		self.horizon = 0
		self.shifts = dict()
		self.staff = list()
		self.daysOff = dict()
		self.shiftOnRequests = dict()
		self.shiftOffRequests = dict()