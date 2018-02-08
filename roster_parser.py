import instance

def ParseHorizon(line, thisInstance):
	# The horizon length in days:
	thisInstance.horizon = int(line)
	thisInstance.cover = [dict() for _ in range(thisInstance.horizon)]

def ParseShifts(line, thisInstance):
	# ShiftID, Length in mins, Shifts which cannot follow this shift | separated
	result = instance.Shift()
	sections = line.split(',')

	result.id = sections[0]
	result.length = int(sections[1])
	result.prohibitNext = set()

	for x in sections[2].split('|'):
		result.prohibitNext.add(x)

	thisInstance.shifts[result.id] = result

def ParseStaff(line, thisInstance):
	# ID, MaxShifts, MaxTotalMinutes, MinTotalMinutes, MaxConsecutiveShifts, MinConsecutiveShifts, MinConsecutiveDaysOff, MaxWeekends
	result = instance.StaffMember()
	sections = line.split(',')

	result.id = sections[0]
	result.maxShifts = dict()
	result.maxTotalMinutes = int(sections[2])
	result.minTotalMinutes = int(sections[3])
	result.maxConsecutiveShifts = int(sections[4])
	result.minConsecutiveShifts = int(sections[5])
	result.minConsecutiveDaysOff = int(sections[6])
	result.maxWeekends = int(sections[7])

	for x in sections[1].split('|'):
		shiftId, maxCount = x.split('=')
		maxCount = int(maxCount)
		# Only add restriction that can be violated
		if (maxCount < thisInstance.horizon):
			result.maxShifts[shiftId] = maxCount
	
	thisInstance.staff[result.id] = result

def ParseDaysOff(line, thisInstance):
	# EmployeeID, DayIndexes (start at zero)
	sections = line.split(',')
	
	staffId = sections[0]
	days = [int(x) for x in sections[1:]]

	thisInstance.staff[staffId].daysOff = days

def ParseShiftOnRequests(line, thisInstance):
	# EmployeeID, Day, ShiftID, Weight
	sections = line.split(',')
	result = instance.ShiftRequest()

	result.id = sections[2]
	result.day = int(sections[1])
	result.weight = int(sections[3])

	thisInstance.staff[sections[0]].shiftOnRequests[result.day] = result

def ParseShiftOffRequests(line, thisInstance):
	# EmployeeID, Day, ShiftID, Weight
	sections = line.split(',')
	result = instance.ShiftRequest()

	result.id = sections[2]
	result.day = int(sections[1])
	result.weight = int(sections[3])

	thisInstance.staff[sections[0]].shiftOffRequests[result.day] = result

def ParseCover(line, thisInstance):
	# Day, ShiftID, Requirement, Weight for under, Weight for over
	result = instance.Cover()
	sections = line.split(',')

	result.day = int(sections[0])
	result.shiftId = sections[1]
	result.requirement =  int(sections[2])
	result.weightForUnder = int(sections[3])
	result.weightForOver = int(sections[4])

	thisInstance.cover[result.day][result.shiftId] = result

parseMethod = {
	'SECTION_HORIZON': ParseHorizon,
	'SECTION_SHIFTS': ParseShifts,
	'SECTION_STAFF': ParseStaff,
	'SECTION_DAYS_OFF': ParseDaysOff,
	'SECTION_SHIFT_ON_REQUESTS': ParseShiftOnRequests,
	'SECTION_SHIFT_OFF_REQUESTS': ParseShiftOffRequests,
	'SECTION_COVER': ParseCover,
}

def LineType(line):
	if line in parseMethod.keys():
	   return line
	else:
		return 'DATA'

def ParseRoster(filename):
	file = open(filename, 'r')
	contents = file.read()
	file.close()

	# filter comments and empty lines in file
	contents = [s for s in contents.split('\n') if (s != '' and s[0] != '#')]
	parseType = None
	currentParseMethod = None
	result = instance.ProblemInstance()

	for line in contents:
		parseType = LineType(line)

		if parseType != 'DATA':
			currentParseMethod = parseMethod[parseType]
		else:
			currentParseMethod(line, result)

	return result
