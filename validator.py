# start class
class StaffMemberResult:
    
    def __init__(self):
        self.id = ''
        self.totalMinutes = 0
        self.minConsecutiveShifts = float('inf')
        self.maxConsecutiveShifts = 0
        self.minConsecutiveDaysOff = float('inf')
        self.weekends = 0
        self.offRequestPenalty = 0
        self.onRequestPenalty = 0
        self.hardViolations = 0
        
    def BuildInfo(self, solution, problem, staffId):
        self.id = staffId
        staffMember = problem.staff[staffId]
        memberSchedule = solution.schedule[staffId]
        lastShift = ''
        shiftsTaken = dict()
        for idx, shift in enumerate(memberSchedule):
            shiftsTaken[shift] = shiftsTaken.get(shift, 0) + 1
            if shift != ' ':
                self.totalMinutes += problem.shifts[shift].length

                if idx in staffMember.shiftOffRequests:
                    self.offRequestPenalty += staffMember.shiftOffRequests[idx].weight
                
                if idx in staffMember.daysOff:
                    self.hardViolations += 1
                
                if lastShift != '' and lastShift != ' ' and shift in problem.shifts[lastShift].prohibitNext:
                    self.hardViolations += 1
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
        
        for shift, count in shiftsTaken.items():
            if staffMember.maxShifts.get(shift, problem.horizon) < count:
                self.hardViolations += 1

        if self.totalMinutes < staffMember.minTotalMinutes:
            self.hardViolations += 1

        if self.totalMinutes > staffMember.maxTotalMinutes:
            self.hardViolations += 1

        if self.minConsecutiveShifts < staffMember.minConsecutiveShifts:
            self.hardViolations += 1

        if self.maxConsecutiveShifts > staffMember.maxConsecutiveShifts:
            self.hardViolations += 1

        if self.minConsecutiveDaysOff < staffMember.minConsecutiveDaysOff:
            self.hardViolations += 1

        if self.weekends > staffMember.maxWeekends:
            self.hardViolations += 1

    def CalculatePenalty(self):
        return self.offRequestPenalty + self.onRequestPenalty
        
        
    def IsValid(self, staffMember):
        return self.hardViolations == 0
# end class
            
def CalculatePenalty(solution, problem):
    totalPenalty = 0
    for staffId in problem.staff.keys():
        staffMemberResult = StaffMemberResult()
        staffMemberResult.BuildInfo(solution, problem, staffId)
        totalPenalty += staffMemberResult.hardViolations * problem.hardConstraintWeight
        totalPenalty += staffMemberResult.CalculatePenalty()
        solution.hardViolations += staffMemberResult.hardViolations
    for day in range(problem.horizon):
        for shift, cover in problem.cover[day].items():
            count = 0
            for schedule in solution.schedule.values():
                if schedule[day] == shift:
                    count += 1

            if cover.requirement < count:
                totalPenalty += (count - cover.requirement) * cover.weightForOver 
            else:
                totalPenalty += (cover.requirement - count) * cover.weightForUnder
    solution.score = totalPenalty
