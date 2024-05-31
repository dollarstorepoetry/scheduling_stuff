from datetime import date, timedelta
import random

class Person:
    def __init__(self, name):
        self.name = name
        self.unavailable_dates = set()  # set of Date objects. using method bc python thinks it's a dictionary otherwise
        
    def add_unavailable_date(self, d):
        self.unavailable_dates.add(d)

    def mark_weekdays_unavailable(self, date_range, weekdays):
        """
        date_range is a an array containing the beginning and end Date
        weekdays is an array containing the weekdays to be marked unavailable as integers
            Note that timedate.weekday() returns 0-6 given Mon-Sun
        """
        # looping through dates as sanctioned by the datetime module
        date_i = date_range[0]
        end_date = date_range[1]
        delta = timedelta(days=1)
        while (date_i <= end_date):
            if (date_i.weekday() in weekdays):
                self.add_unavailable_date(date_i)
            date_i += delta

class Employee(Person):
    def __init__(self, name, start_date, end_date):
        Person.__init__(self, name)
        self.employment_range = [start_date, end_date]
        self.available_dates = set()
        self.update_available_dates()

    def update_available_dates(self):
        """
        Reset currently available dates and update from the bottom up
        given the employment range and unavailable dates
        """
        self.available_dates = set()
        # looping through dates as sanctioned by the datetime module
        date_i = self.employment_range[0]
        end_date = self.employment_range[1]  # inefficient but saves rewriting code :p
        delta = timedelta(days=1)
        while (date_i <= end_date):
            if (date_i not in self.unavailable_dates):
                self.available_dates.add(date_i)
            date_i += delta

    def mark_weekdays_unavailable(self, weekdays):
        """
        date_range is a an array containing the beginning and end Date
        weekdays is an array containing the weekdays to be marked unavailable as integers
            Note that timedate.weekday() returns 0-6 given Mon-Sun
        """
        # looping through dates as sanctioned by the datetime module
        date_i = self.employment_range[0]
        end_date = self.employment_range[1]  # inefficient but saves rewriting code :p
        delta = timedelta(days=1)
        while (date_i <= end_date):
            if (date_i.weekday() in weekdays):
                self.add_unavailable_date(date_i)
                self.available_dates.remove(date_i)  
                # ^ doing this instead of self.update_available_dates()
            date_i += delta

def shift_scheduler(employment_range, list_employees, num_total_shifts):
    """
    This method will schedule shifts for employees given the
    days that they are unavailable.
    Returns the map from employees to shifts
    """
    # set up variables and stuff
    employee_shifts_map = {} #dictionary
    shifts_per_employee = [] # list containing sets of shifts to be associated to each employee. probably don't work with this directly
    taken_shifts = set() # just a set with all the shifts
    min_shifts_per_employee = num_total_shifts // len(list_employees)
    for i, emp in enumerate(list_employees):
        shifts_per_employee.append(set())
        employee_shifts_map.update({emp: shifts_per_employee[i]})

    """
    things that should be considered errors if they happen:
    an employee has less shifts than min_shifts_per_employee
    """
    # i don't have a better algorithm rn. RANDOM ASSIGNMENT BAYBEEEE
    date_i = employment_range[0]
    end_date = employment_range[1]  # inefficient but saves rewriting code :p
    delta = timedelta(days=1)
    while (date_i <= end_date):
        possible_employees = []
        for emp in list_employees:
            if len(employee_shifts_map[emp]) < min_shifts_per_employee \
                    and date_i in emp.available_dates:
                possible_employees.append(emp)

        if len(possible_employees) > 0:
            employee_shifts_map[random.choice(possible_employees)].add(date_i)
            taken_shifts.add(date_i)
        else:
            print(f"Date {date_i.ctime()} has no available employees to take.")
        date_i += delta
    
    return employee_shifts_map

def main():
    contract_range = (date(2024, 6, 1), date(2024, 6, 30))
    nick = Employee("Nick", contract_range[0], contract_range[1])
    joseph = Employee("Joseph", contract_range[0], contract_range[1])
    nick.mark_weekdays_unavailable([1,3])
    joseph.mark_weekdays_unavailable([4,5,6])
    list_employees = [nick, joseph]
    doink = shift_scheduler(contract_range, list_employees, 30)
    for emp in doink.keys():
        print(emp.name)
        shifts = doink[emp]
        for s in shifts:
            print(s.ctime())
        print()


if __name__ == '__main__':
    main()
