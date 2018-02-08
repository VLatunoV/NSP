# start class
class StaffMemberResult:
    
    def __init__(self):
        self.id = ''
        self.totalMinutes = 0
        self.consecutiveShifts = 0
        self.consecutiveDaysOff = 0
        self.weekends = 0
        self.prohibitedShiftChecked = True
        self.maxShiftChecked = True
        self.daysOffChecked = True
        self.offRequestPenalty = 0
        self.onRequestPenalty = 0
        
    def build_info(self, solution, problem, id):
        self.id = id
        member_shifts = solution[id]
        curr_consecutive_shifts = 0
        curr_consecutive_daysoff = 0
        last_shift = ''
        for idx, shift in enumerate(member_shifts):           
            if shift != ' ':
                if (idx in problem.staff[id].shiftOffRequests):
                    self.offRequestPenalty += problem.staff[id].shiftOffRequests[idx].weight
                
                if (idx in problem.staff[id].daysOff):
                    self.daysOffChecked = False
                
                if (last_shift in problem.shifts and shift in problem.shifts[last_shift].prohibitNext):
                    self.prohibitedShiftChecked = False
                last_shift = shift
                
                if (idx + 1) % 7 == 0:
                    self.weekends += 1

                self.totalMinutes += problem.shifts[shift].length 
                curr_consecutive_shifts += 1
                if self.consecutiveDaysOff < curr_consecutive_daysoff:
                    self.consecutiveDaysOff = curr_consecutive_daysoff
                curr_consecutive_daysoff = 0
            else:
                if (idx in problem.staff[id].shiftOnRequests):
                    self.onRequestPenalty += problem.staff[id].shiftOnRequests[idx].weight
                
                if (idx + 1) % 7 == 0 and member_shifts[idx] != ' ': 
                    self.weekends += 1
                
                curr_consecutive_daysoff += 1
                if self.consecutiveShifts < curr_consecutive_shifts:
                    self.consecutiveShifts = curr_consecutive_shifts
                curr_consecutive_shifts = 0
                
        if self.consecutiveDaysOff < curr_consecutive_daysoff:
                    self.consecutiveDaysOff = curr_consecutive_daysoff
        if self.consecutiveShifts < curr_consecutive_shifts:
                    self.consecutiveShifts = curr_consecutive_shifts
        
        for key in problem.staff:
            if key in problem.staff[id].maxShifts and problem.staff[id].maxShifts[key] < len([x for x in member_shifts if x == key]):
                self.maxShiftChecked = False
        
    def calc_penalty(self):
        return self.offRequestPenalty + self.onRequestPenalty
        
        
    def is_valid(self, problem):
        return self.maxShiftChecked and \
                self.prohibitedShiftChecked and \
                self.totalMinutes >= problem.staff[self.id].minTotalMinutes and \
                self.totalMinutes <= problem.staff[self.id].maxTotalMinutes and \
                self.consecutiveShifts >= problem.staff[self.id].minConsecutiveShifts and \
                self.consecutiveShifts <= problem.staff[self.id].maxConsecutiveShifts and \
                self.consecutiveDaysOff >= problem.staff[self.id].minConsecutiveDaysOff and \
                self.weekends <= problem.staff[self.id].maxWeekends
# end class

def validateSolution(solution, problem):
    is_valid = True
    for staff in problem.staff:
        staff_res = StaffMemberResult()
        staff_res.build_info(solution.schedule, problem, staff)
        is_valid = is_valid and staff_res.is_valid(problem)
        if (not is_valid):
            break
        return is_valid
            
def calculatePenalty(solution, problem):
    staff_penalty = 0
    for staff in problem.staff:
        staff_res = StaffMemberResult()
        staff_res.build_info(solution.schedule, problem, staff)
        staff_penalty += staff_res.calc_penalty()
    cover_penalty = 0
    for day in range(problem.horizon):
        for shift in problem.shifts:
            for cover in [cover[shift] for cover in problem.cover if cover[shift].day == day]:
                schedule_day = [solution.schedule[key][day] for key in solution.schedule]
                diff = cover.requirement - len([x for x in schedule_day if x == cover.shiftId])
                if diff < 0:
                    cover_penalty += (-diff) * cover.weightForOver 
                else:
                    cover_penalty += diff* cover.weightForUnder
    return staff_penalty + cover_penalty
