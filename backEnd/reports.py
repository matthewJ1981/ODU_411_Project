from statistics import mean

class Reports:
    #Use the backend for database
    def __init__(self, backend):
        self.backend = backend

    #Abstract query
    def query(self, query, values = ()):
        return self.backend.db.customQuery(query, values)

    #Get all input data entries, and the time between mouse clicks.  Return the min, max, average, and list of differences as a tuple
    def adminInactivity(self):
        #List of time between mouse clicks in seconds   
        dts = []
        #Get all child id's from the input data table
        print(self.query("SELECT DISTINCT child_id from input_data", ()))
        
        #for cid in self.backend.db.inputData.getField("child_id"):
        for cid, in self.query("SELECT DISTINCT child_id from input_data"):
            #Call self.childInactivity() for each child id and append the time between mouse clicks to the dts list
            for seconds in self.childInactivity(cid)[3]:
                dts.append(seconds)

        #Calculae the min, max, and mean, and return all as a tuple including the dts list
        if dts == []:
            return None
        else:            
            return (min(dts), max(dts), mean(dts), dts)

    #Get all input data for provided child id. Return the min, max, average, and list of differences as a tuple
    def childInactivity(self, childID):
        def sortBy(tup):
            return tup[1]

        def changeToDateTime(list):
            newList = []
            for t in list:
                newList.append((t[0], self.backend.formatAsDatetimeMicro(t[1]), t[2], t[3], t[4], t[5]))

            return newList

        result = changeToDateTime(self.backend.db.inputData.getByChild(childID))
        result.sort(key = sortBy)
        #print(result)

        dts = []
        #Get difference in  input data entry i - (i - 1) in seconds
        for i, x in enumerate(result):
            if i > 0:
                dts.append((result[i][1] - result[i - 1][1]).seconds)

        #print(dts)
        #Calculae the min, max, and mean, and return all as a tuple including the dts list  
        if dts == []:
            return None
        else:
            return (min(dts), max(dts), mean(dts), dts)

    #Grammar formatting
    def formatEnd(self, seconds):
        if seconds == 1:
            return " second."
        else:
            return " seconds."

    #Get all log entries and return the total navigation attemps, # of successful attemps, and the percent of succesful as a tuple
    def adminNavigation(self):
        total = 0
        successful = 0
        for cid, in self.query("SELECT DISTINCT child_id from log_entry"):
            tot, suc, per = self.childNavigation(cid)
            total += tot
            successful += suc

        if total == 0:
            return None
        else:
            return (total, successful, round(successful / total * 100, 0))
            
    #Get log entries for the provided child and return the total navigation attemps, # of successful attemps, and the percent of succesful as a tuple
    def childNavigation(self, childID):
        total = 0
        successful = 0

        for x, in self.query("SELECT navigation_state from log_entry WHERE child_id = %s", (childID,)):
            total += 1
            successful += x

        if total == 0:
            return None
        else:
            return (total, successful, round(successful / total * 100, 0))

if __name__ == "__main__":
    from backEnd import BackEnd

    reports = Reports(BackEnd())

    while(True):
        while(True):
            print("Reports\n")
            option1 = "All time between mouse clicks (1)\n"
            option2 = "All percentage of Navigation success (2)\n"
            option3 = "Time between mouse clicks for a specific child (3)\n"
            option4 = "Percentage of navigation success for a specific chid (4)"
            selection = int(input(option1 + option2 + option3 + option4 + "\n:"))
            if selection < 1 or selection > 4:
                print("Invalid selection\n")
            else:
                break

        if selection == 1:
            #All input data 
            stats = reports.adminInactivity()
            if stats != ():
                _min, _max, _avg, _dts = stats
                print("The minimum time between mouse clicks across all children is: " + str(_min) + reports.formatEnd(_min))
                print("The maximum time between mouse clicks across all children is: " + str(_max) + reports.formatEnd(_max))
                print("The average time between mouse clicks across all children is: " + str(round(_avg, 2)) + reports.formatEnd(_avg))
        elif selection == 2:
            #All navigation data
            stats = reports.adminNavigation()
            if stats != None:
                _total, _succesful, _percent = stats
                print("The percentage of successful navigation across all children is: " + str(_percent) + "%.")
        elif selection == 3:
            cid = int(input("Enter the id of the child: "))

            #Input data for child
            stats = reports.childInactivity(cid)
            if stats != None:
                _min, _max, _avg, _dts = stats
                print("The minimum time between mouse clicks for child " + str(cid) + " is: " + str(_min) + reports.formatEnd(_min))
                print("The maximum time between mouse clicks for child " + str(cid) + " is: " + str(_max) + reports.formatEnd(_max))
                print("The average time between mouse clicks for child " + str(cid) + " is: " + str(round(_avg, 2)) + reports.formatEnd(_avg))
            else:
                print("No data for provided child ID")

        elif selection == 4:
            cid = int(input("Enter the id of the child: "))

            #Navigation data for child
            stats = reports.childNavigation(cid)
            if stats != None:
                _total, _succesful, _percent = stats
                print("The percentage of successful navigation for child " + str(cid) + " is: " + str(_percent) + "%.")
            else:
                print("No data for provided child ID")

        again = input("Make another selection? (Y/N): ")
        if again[0] != 'Y' and again[0] != 'y':
            break
