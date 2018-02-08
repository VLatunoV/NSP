# start class
class StaffMemberResult:
    
    def __init__(self):
        self.id = ''
        self.totalMinutes = 0
        self.minConsecutiveShifts = float('inf')
        self.maxConsecutiveShifts = 0
        self.minConsecutiveDaysOff = float('inf')
        self.weekends = 0
        self.prohibitedShiftChecked = True
        self.maxShiftChecked = True
        self.daysOffChecked = True
        self.offRequestPenalty = 0
        self.onRequestPenalty = 0
        
    def BuildInfo(self, solution, problem, staffId):
        self.id = staffId
        staffMember = problem.staff[staffId]
        memberSchedule = solution.schedule[staffId]
        lastShift = ''
        for idx, shift in enumerate(memberSchedule):
            if shift != ' ':
                self.totalMinutes += problem.shifts[shift].length

                if idx in staffMember.shiftOffRequests:
                    self.offRequestPenalty += staffMember.shiftOffRequests[idx].weight
                
                if idx in staffMember.daysOff:
                    self.daysOffChecked = False
                    print('day off violated')
                
                if lastShift in problem.shifts and shift in problem.shifts[lastShift].prohibitNext:
                    self.prohibitedShiftChecked = False
                    print('prohibited shift')
            else:
                if idx in staffMember.shiftOnRequests:
                    self.onRequestPenalty += staffMember.shiftOnRequests[idx].weight

            lastShift = shift
        
        lastShift = memberSchedule[0]
        consecutiveShifts = 0
        consecutiveDaysOff = 0
        if lastShift != ' ':
            consecutiveShifts += 1

        for shift in memberSchedule[1:]:
            if shift != ' ':
                if lastShift == ' ' and self.maxConsecutiveShifts != 0:
                    if self.minConsecutiveDaysOff > consecutiveDaysOff:
                        self.minConsecutiveDaysOff = consecutiveDaysOff

                consecutiveDaysOff = 0
                consecutiveShifts += 1
            else:
                if lastShift != ' ':
                    if self.maxConsecutiveShifts < consecutiveShifts:
                        self.maxConsecutiveShifts = consecutiveShifts
                    if self.minConsecutiveShifts > consecutiveShifts:
                        self.minConsecutiveShifts = consecutiveShifts
                
                consecutiveShifts = 0
                consecutiveDaysOff += 1
            lastShift = shift
        
        if consecutiveShifts != 0:
            if self.maxConsecutiveShifts < consecutiveShifts:
                self.maxConsecutiveShifts = consecutiveShifts
            if self.minConsecutiveShifts > consecutiveShifts:
                self.minConsecutiveShifts = consecutiveShifts

        totalWeekends = int(problem.horizon / 7)
        weekendWorking = [[memberSchedule[week*7 + x] != ' ' for x in [5, 6]] for week in range(totalWeekends)]
        if problem.horizon % 7 == 6:
            weekendIndex.append([memberSchedule[problem.horizon - 1] != ' '])
        for weekend in weekendWorking:
            if any(weekend):
                self.weekends += 1
        
        for key in problem.staff:
            if key in staffMember.maxShifts and staffMember.maxShifts[key] < len([x for x in memberSchedule if x == key]):
                self.maxShiftChecked = False
                print('maxShifts reached')
        
    def CalculatePenalty(self):
        return self.offRequestPenalty + self.onRequestPenalty
        
        
    def IsValid(self, staffMember):
        return self.maxShiftChecked and \
                self.prohibitedShiftChecked and \
                self.totalMinutes >= staffMember.minTotalMinutes and \
                self.totalMinutes <= staffMember.maxTotalMinutes and \
                self.minConsecutiveShifts >= staffMember.minConsecutiveShifts and \
                self.maxConsecutiveShifts <= staffMember.maxConsecutiveShifts and \
                self.minConsecutiveDaysOff >= staffMember.minConsecutiveDaysOff and \
                self.weekends <= staffMember.maxWeekends and \
                self.daysOffChecked
        '''print (self.id)
        if not(self.totalMinutes >= staffMember.minTotalMinutes):
            print('Total minutes exceed')
            return False
        if not(self.totalMinutes <= staffMember.maxTotalMinutes):
            print('Total minutes too low')
            return False
        if not(self.minConsecutiveShifts >= staffMember.minConsecutiveShifts):
            print('minConsecutiveShifts violated', self.minConsecutiveShifts)
            return False
        if not(self.maxConsecutiveShifts <= staffMember.maxConsecutiveShifts):
            print('maxConsecutiveShifts violated')
            return False
        if not(self.minConsecutiveDaysOff >= staffMember.minConsecutiveDaysOff):
            print('minConsecutiveDaysOff violated', self.minConsecutiveDaysOff)
            return False
        if not(self.weekends <= staffMember.maxWeekends):
            print('maxWeekends reached')
            return False
        return True'''
# end class

def ValidateSolution(solution, problem):
    for staffId in problem.staff.keys():
        staffMemberResult = StaffMemberResult()
        staffMemberResult.BuildInfo(solution, problem, staffId)
        if not staffMemberResult.IsValid(problem.staff[staffId]):
            return False
    return True
            
def CalculatePenalty(solution, problem):
    staffPenalty = 0
    for staffId in problem.staff.keys():
        staffMemberResult = StaffMemberResult()
        staffMemberResult.BuildInfo(solution, problem, staffId)
        staffPenalty += staffMemberResult.CalculatePenalty()
    coverPenalty = 0
    for day in range(problem.horizon):
        for shift, cover in problem.cover[day].items():
            count = 0
            for schedule in solution.schedule.values():
                if schedule[day] == shift:
                    count += 1

            if cover.requirement < count:
                coverPenalty += (count - cover.requirement) * cover.weightForOver 
            else:
                coverPenalty += (cover.requirement - count) * cover.weightForUnder
    return staffPenalty + coverPenalty
