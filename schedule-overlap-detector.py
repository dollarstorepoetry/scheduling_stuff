class Person:
    def __init__(self, days):
        # days is the array of time slots - each time slot is stored
        # as a two-component array of minutes
        # it may be declared as strings. but this constructor will
        # automatically turn those things to minutes
        if type(days[0][0][0]) == str:
            for i in days:
                for j in i:
                    for index in range(len(j)):
                        if type(j[index]) == str:
                            j[index] = Person.convert_time_to_minute(j[index])
        self.days = days

        
    def convert_time_to_minute(time, is24hr=True):
        # assumption: time is in the form "hh:mm".
        time = time.split(":")
        minutes = int(time[0])*60 + int(time[1].split(" ")[0])

        # worry about this shit later i cba
        # this is 24 hour handling
        if not is24hr:
            doink = time[1].split(" ")
            if doink[1].upper() == "PM":
                minutes += 60*12
            elif doink[1].upper() != "AM":
                raise Exception
            
        return minutes

    def convert_minute_to_time(minutes, is24hr=True):
        hours = str(minutes // 60).zfill(2)
        minutes = str(minutes % 60).zfill(2)
        time = f"{hours}:{minutes}"
        return time   

    def add_taken_time_slot(self, day, beginning, end):
        # takes in beginning and end times as strings,  
        # converts them to minutes, and adds the range 
        if type(day) == str:
            # convert day to an int
            pass
        elif type(day) == int:
            pass

        # insert time slot at appropriate position
        for i, arr in enumerate(self.days):
            if arr[0] <= beginning:
                self.days.insert(i, [beginning, end])
                # obviously add some error handling at some point

    def return_free_minutes(self):
        # this is NOT the most efficient algorithm
        free_minutes = [[] for i in range(len(self.days))]
        i = 0
        for day in self.days:
            for minute in range(60*24):
                ass = False
                for rangy in day:
                    if (rangy[0] <= minute <= rangy[1]):
                        ass = True
                        break
                if not ass:
                    free_minutes[i].append(minute)
            print(free_minutes)
            i += 1

        # remove the duplicates this way because
        # i don't wanna leetcode how to fix this algorithm rn

        return free_minutes

    def return_free_times(self):
        print(self.days)
        free_minutes = self.return_free_minutes()
        free_times = [[] for i in range(len(self.days))]
        beginning = 0
        for day in range(len(self.days)):
            for i in range(len(free_minutes)):
                if i != 0:
                    if free_minutes[day][i] > free_minutes[day][i-1] + 1 or i == len(free_minutes[day]) - 1:
                        # print(i, type(beginning))
                        beginning_time = Person.convert_minute_to_time(free_minutes[day][beginning])
                        end_time = Person.convert_minute_to_time(free_minutes[day][i])                  
                        free_times[day].append([beginning_time, end_time])
                        beginning = i
        return free_times
    
    def return_combined(self, other):
        # combine two types of people
        # assumption: other is of type Person
        # days are of same length. they better be
        newdays = []
        for i in range(len(self.days)):
            day_i = []
            day_i.append(self.days[i] + other.days[i])
            newdays.append(day_i)
        return Person(newdays)
    

def main():
    chris_list = [
        [["8:30","9:45"],["16:00","18:45"]],
        [["10:00","11:15"],["17:30","18:45"]],
        [["8:30","12:30"],["16:00","18:45"]],
        [["10:00","11:15"],["17:30","18:45"]]
    ]
    nick_list = [
        [["11:30","14:15"],["16:00","17:15"]],
        [["11:30","14:15"],["16:00","17:15"]],
        [["11:30","12:45"],["16:00","17:15"]],
        [["11:30","14:15"],["16:00","17:15"]]
    ]
    colin_list = [
        [["11:30","12:45"],["14:30","17:15"]],
        [["10:00","12:45"],["15:00","15:45"]],
        [["11:30","12:45"],["14:30","17:15"]],
        [["10:00","12:45"],["15:00","16:40"]]
    ]
    keval_list = [
        [["9:00","9:40"],["14:30","15:45"]],
        [["10:00","14:15"]],
        [["9:00","9:40"],["14:30","15:45"]],
        [["10:00","14:15"]]
    ]
    chris = Person(chris_list)
    nick = Person(nick_list)
    colin = Person(colin_list)
    keval = Person(keval_list)

    # chris_free = chris.return_free_minutes()
    nick_free = nick.return_free_minutes()
    # colin_free = colin.return_free_minutes()
    # keval_free = keval.return_free_minutes()

    # all_free = [[] for i in range(4)]
    # for j in range(4):
    #     for i in range(60*24):
    #         if i in chris_free[j] and i in nick_free[j] and i in colin_free[j] and i in keval_free[j]:
    #             all_free[j].append(i)

    print(nick.return_free_times())


main()
