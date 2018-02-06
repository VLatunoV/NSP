import instance

def ParseHorizon(line):
	# The horizon length in days:
	return int(line)

def ParseShifts(line):
	# ShiftID, Length in mins, Shifts which cannot follow this shift | separated
	result = instance.Shift()
	sections = line.split(',')

	result.id = sections[0]
	result.length = int(sections[1])
	result.prohibitNext = set()

	if len(sections) == 3:
		for x in sections[2].split('|'):
			result.prohibitNext.add(x)

	return result

def ParseStaff(line, horizon = float('inf')):
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
	# Maximum working weekends
	result.maxWeekends = int(sections[7])

	for x in sections[1].split('|'):
		shiftId, maxCount = x.split('=')
		maxCount = int(maxCount)
		# Only add restriction that can be violated
		if (maxCount < horizon):
			result.maxShifts[shiftId] = maxCount
	return result

def ParseDaysOff(line):
	# EmployeeID, DayIndexes (start at zero)
	sections = line.split(',')
	
	staffID = sections[0]
	days = [int(x) for x in sections[1:]]

	return staffID, days

def ParseShiftRequests(line):
	# EmployeeID, Day, ShiftID, Weight
	sections = line.split(',')
	return sections[0], int(sections[1]), sections[2], int(sections[3])

def ParseCover(line):
	# Day, ShiftID, Requirement, Weight for under, Weight for over
	result = instance.Cover()
	sections = line.split(',')

	result.day = int(sections[0])
	result.shiftId = sections[1]
	result.requirement =  int(sections[2])
	result.weightForUnder = int(sections[3])
	result.weightForOver = int(sections[4])

	return result

def AddHorizon(horizon, instance):
	instance.horizon = horizon

def AddShifts(shift, instance):
	instance.shifts[shift.id] = shift

def AddStaff(staff, instance):
	instance.staff.append(staff)

def AddDaysOff(staffId, days, instance):
	instance.daysOff[staffId] = days

def AddShiftOnRequests(staffId, day, shiftId, weight, instance):
	instance.shiftOnRequests[staffId].append((day, shiftId, weight))

def AddShiftOffRequests(staffId, day, shiftId, weight, instance):
	instance.shiftOffRequests[staffId].append((day, shiftId, weight))

def AddCover(line, instance):
	# Day, ShiftID, Requirement, Weight for under, Weight for over
	result = instance.Cover()
	sections = line.split(',')

	result.day = int(sections[0])
	result.shiftId = sections[1]
	result.requirement =  int(sections[2])
	result.weightForUnder = int(sections[3])
	result.weightForOver = int(sections[4])

	return result

_parse_method = {
	'SECTION_HORIZON': ParseHorizon,
	'SECTION_SHIFTS': ParseShifts,
	'SECTION_STAFF': ParseStaff,
	'SECTION_DAYS_OFF': ParseDaysOff,
	'SECTION_SHIFT_ON_REQUESTS': ParseShiftRequests,
	'SECTION_SHIFT_OFF_REQUESTS': ParseShiftRequests,
	'SECTION_COVER': ParseCover,
}

def LineType(line):
	if line in _parse_method.keys():
	   return line
	else:
		return 'DATA'

def ParseRoster(filename):
	file = open(filename, 'r')
	contents = file.read()
	file.close()

	# filter comments and empty lines in file
	contents = [s for s in contents.split('\n') if (s != '' and s[0] != '#')]

	current_parse_type = None
	for line in contents:
		current_parse_type = LineType(line)

		if current_parse_type == 'SECTION_HORIZON':
			pass
		elif current_parse_type == 'SECTION_SHIFTS':
			pass
		elif current_parse_type == 'SECTION_STAFF':
			pass
		elif current_parse_type == 'SECTION_DAYS_OFF':
			pass
		elif current_parse_type == 'SECTION_SHIFT_ON_REQUESTS':
			pass
		elif current_parse_type == 'SECTION_SHIFT_OFF_REQUESTS':
			pass
		elif current_parse_type == 'SECTION_COVER':
			pass
		else:
			pass

	return contents

s = ParseShiftRequests('A,2,D,2')
print (s)