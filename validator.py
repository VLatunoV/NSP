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
        
    def build_info(self, solution, problem, id):
        self.id = id
        member_shifts = solution[member];
        curr_consecutive_shifts = 0
        curr_consecutive_daysoff = 0
        last_shift = ''
        for idx, shift in enumerate(member_shifts):           
            if shift != ' ':
                if (problem.shifts[last_shift] and shift in problem.shifts[last_shift].prohibitNext):
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
        
        for key in problem.staff[member]:
            if problem.staff[member].maxShifts[key] < len([x for x in member_shifts if x == key]):
                self.maxShiftChecked = False
        
    def calc_penalty(self, solution, problem):
        print('Not implemented')
        
    def is_valid(self, problem):
        return self.maxShiftChecked and \
                self.prohibitedShiftChecked and \
                self.totalMinutes >= problem.staff[member].minTotalMinutes and \
                self.totalMinutes <= problem.staff[member].maxTotalMinutes and \
                self.consecutiveShifts >= problem.staff[member].minConsecutiveShifts and \
                self.consecutiveShifts <= problem.staff[member].maxConsecutiveShifts and \
                self.consecutiveDaysOff >= problem.staff[member].minConsecutiveDaysOff and \
                self.weekends <= problem.staff[member].maxWeekends
# end class

def ValidateSolution(solution, problem):
    is_valid = True
    for staff in problem.staff:
        staff_res = StaffMemberResult()
        staff_res.build(solution, problem, staff)
        is_valid = is_valid and staff_res.is_valid(problem)
        if (not is_valid):
            break
            
def calculatePenalty(solution, problem):
    sum_amm = 0
    for staff in problem.staff:
        staff_res = StaffMemberResult()
        staff_res.build(solution, problem, staff)
        sum_amm += staff_res.calc_penalty(solution, problem)