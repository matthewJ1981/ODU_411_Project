import os, sys
sys.path.insert(0, os.path.abspath("../backEnd"))

from database import database
from backEnd import BackEnd
import datetime as dt
from dateutil import tz
import time

##google stuff
import datetime
import os.path


if __name__ == "__main__":

    try:
        print("Connecting to database")
        backend = BackEnd()
        db = backend.db
        for i, arg in enumerate(sys.argv):
            if arg == "y":
                print("Resetting database tables")
                db.createTestDB()

        db.useDB()
        print("Call removeAll()")
        db.removeAll()
    except Exception as e:
        print(e)
    else:  
        try:
            print("Adding bubble")
            b1 = db.bubble.add("b1")
        except Exception as e:
            print(e)
            raise
        # try:
        #     print("Adding user types")
        #     t1 = db.userType.add("Parent")
        #     t2 = db.userType.add("Child")
        # except:
        #     print("User types already added")

        try:
            print("Adding Parents")
            #p1
            karenID = db.parent.add("p1", "12345678", "abc@gmail.com", "Karen", "Smith", "555-123-4568")
            #p2
            johnID = db.parent.add("p2", "12345678", "parent2@littlelearners.com", "Karen", "Smith", "213-345-6778")
        except Exception as e:
            print(e)
            raise

        try:
            print("Adding Parents to bubble")
            db.memberOf.add(karenID, b1)
        except Exception as e:
            print(e)
            raise

        try:
            print("Adding children")
            ch1 = db.child.add("Who", 4, karenID)
            
            #ch2
            timmyID = db.child.add("Timmy", 7, johnID, image = 'student/frontEnd/images/timmy.jpg')
            #ch3
            erinID = db.child.add("Erin", 6, johnID, image = 'student/frontEnd/images/Erin.jpg')

            className="Computer Math"
            teacherName="Ms. Carleson"
            calendarID="c_l5eqg00juie3osvaa9cifpisi0@group.calendar.google.com"


            backend.newClass(className,teacherName,calendarID,erinID)


        except Exception as e:
            print(e)
            raise

        # try:
        #     print("Adding error codes")
        #     e1 = db.errorCode.add(0, "Navigation error")
        #     e2 = db.errorCode.add(1, "Some other error")
        # except:
        #     raise

        try:
            print("Adding Classes")
            
            #commented this out since we are moving to real test data
            #cl2 = db._class.add("French", "Tom")
            #cl3 = db._class.add("Physics", "Joseph")
            #cl4 = db._class.add("Biology", "Mike")
            #cl5 = db._class.add("Computer Science", "Mike")
        except Exception as e:
            print(e)
            raise

        try:
            print("Adding children to classes")
            #db.enrolledIn.add(ch1, cl2) # Bob -> French

            #db.enrolledIn.add(ch2, cl2) # John -> French
            #db.enrolledIn.add(ch2, cl4) # John -> Biology
            #db.enrolledIn.add(ch2, cl5) # John -> Computer Science


            #db.enrolledIn.add(ch3, cl3) # Alice -> Physics
        except Exception as e:
            print(e)
            raise

        try:
            print("Adding Activities")

            #a2 = db.activity.add("Reading", cl2,  True)     # French -> Reading
            #a3 = db.activity.add("Lab", cl3, True)         # Physics -> Lab
            #a4 = db.activity.add("Lecture", cl4,  True)     # Biology -> Lecture
            #a5 = db.activity.add("Network", cl5,  True)     # Computer -> Network
        except Exception as e:
            print(e)
            raise
        
        try:
            print("Adding macro elements")
            #me1 = db.macroElement.add(1, ch1,  a1, "Name", "www.google.com", False, "in", "pathj", b'100', 50, 60)
            #me1 = db.macroElement.add(2, ch1, a1, "Name", "www.google.com", False, "in", "path", b'120', 80, 100)
        except Exception as e:
            print(e)
            raise

        try:
            print("Adding Schedule items")
            
            # now = backend.convertToLocal(dt.datetime.utcnow()) # current date time
            # #print(now)
            # now = now.astimezone(tz.tzlocal())
            # #print(now)
            # now = backend.convertToUtc(now)
            #now = backend.UTCNow()
            #fiveMin = now + dt.timedelta(minutes = 5) 
            #tenMin = now + dt.timedelta(minutes = 10)

            #print(backend.formatAsString(now))
            
            # yesterday schedule
            #yesterday = now - dt.timedelta(days = 1) 
            #s10 = db.scheduleItem.add(backend.formatAsString(yesterday), "5", a2)
            
            ##google time
            #s11 = db.scheduleItem.add(backend.formatAsString(classTime_obj), "5", a1)
            
            # tomorrow schedule
            #tomorrow = now + dt.timedelta(days = 1) 
            #s8 = db.scheduleItem.add(backend.formatAsString(tomorrow), "5", a2)

            #s3 = db.scheduleItem.add(backend.formatAsString(now), "5", a2)
            #s4 = db.scheduleItem.add(backend.formatAsString(fiveMin), "5", a4)
            #s5 = db.scheduleItem.add(backend.formatAsString(tenMin), "5", a5)
            #s7 = db.scheduleItem.add(backend.formatAsString(fiveMin), "5", a3)
            # s3 = db.scheduleItem.add(backend.formatAsString(now), "5", a2)
            # s4 = db.scheduleItem.add(backend.formatAsString(fiveMin), "5", a4)
            # s5 = db.scheduleItem.add(backend.formatAsString(tenMin), "5", a5)
            # s6 = db.scheduleItem.add(backend.formatAsString(now), "5", a1)
            # s7 = db.scheduleItem.add(backend.formatAsString(fiveMin), "5", a3)
            # s3 = db.scheduleItem.add(now.strftime("%Y-%m-%d %H:%M:%S"), "5", a2)
            # s4 = db.scheduleItem.add(fiveMin.strftime("%Y-%m-%d %H:%M:%S"), "5", a4)
            # s5 = db.scheduleItem.add(tenMin.strftime("%Y-%m-%d %H:%M:%S"), "5", a5)
            # s6 = db.scheduleItem.add(now.strftime("%Y-%m-%d %H:%M:%S"), "5", a1)
            # s7 = db.scheduleItem.add(fiveMin.strftime("%Y-%m-%d %H:%M:%S"), "5", a3)
        except Exception as e:
            print(e)
            raise
            
        # try:
        #     print("Adding Navigation steps for schedule items")
        #     db.navElemType.add("URL")
        #     n1 = db.navigationStep.add("Element", "URL", 1, s3, None)
        #     n2 = db.navigationStep.add("Elem", "URL", 2, s3, None)
        #     n3 = db.navigationStep.add("More", "URL", 1, s3, None)
        # except:
        #     raise

        try:
            print("Adding log entries")
            db.logEntry.add(ch1, backend.formatAsString(backend.UTCNow()), False)
            time.sleep(1)
            db.logEntry.add(timmyID, backend.formatAsString(backend.UTCNow()), True)
        except Exception as e:
            print(e)
            raise

        try:
            print("Adding data input")
            db.inputData.add(backend.formatAsStringMicro(backend.UTCNowMicro()), ch1, 78, 98, "Text")
            time.sleep(1)
            db.inputData.add(backend.formatAsStringMicro(backend.UTCNowMicro()), ch1, 334, 124, None)
        except Exception as e:
            print(e)
            raise

        try:
            print("Adding help request")
            db.helpRequest.add(backend.formatAsString(backend.UTCNow()), ch1, "Help")
        except Exception as e:
            print(e)
            raise

        try:
            print("Adding help reponse")
            db.helpResponse.add(backend.formatAsString(backend.UTCNow()), karenID, ch1, "Go Away")
        except Exception as e:
            print(e)
            raise
        
        print("Bubbles:")
        for b in db.bubble.getAll():
            print(b)

        print("Parents:")
        for p in db.parent.getAll():
            print(p)

        print("Parent in Bubbles")
        for p in db.memberOf.getAll():
            print(p)

        print("Chilren:")
        for c in db.child.getAll():
            print(c)

        # print("Users:")
        # for u in db.user.getAll():
        #     print(u)

        print("Classes:")
        for c in db._class.getAll():
            print(c)  

        # print("User types")
        # for t in db.userType.getAll():
        #     print(t)

        # print("Error Codes")
        # for e in db.errorCode.getAll():
        #     print(e)

        print("Log entries")
        for e in db.logEntry.getAll():
            print(e)

        print("Input data")
        for d in db.inputData.getAll():
            print(d)

        print("Children in class: ")
        for h in db.enrolledIn.getAll():
            print(h)

        print("Acitivities:")
        for a in db.activity.getAll():
            print(a)

        print("Macro Elements")
        for m in db.macroElement.getAll():
            print(m)

        print("Schedule items")
        for s in db.scheduleItem.getAll():
            print(s)

        # print("Navigation Steps")
        # for s in db.navigationStep.getAll():
        #     print(s)

        # print("Navigation Element Types:")
        # for t in db.navElemType.getAll():
        #     print(t)
        
        print("Help requests")
        for r in db.helpRequest.getAll():
            print(r)

        print("Help responses")
        for r in db.helpResponse.getAll():
            print(r)

        print("Classes child " + str(ch1)  +  " is in:")
        for c in db.getClassesForChild(ch1):
            print(c)

        print("Children in class " + str(cl1) + ":")
        for c in db.getChildrenInClass(cl1):
            print(c)    
        
        print("Schedule items for class " + str(cl1) + ":")
        for s in db.scheduleItem.getByActivity(a1):
            print(s)

        print("Schedule items for child " + str(ch1) + ":")
        for s in db.getItemsForChild(ch1):
            print(s)
    
        print("Macro Elements for Activity " + str(a1) + ":")
        for s in db.macroElement.getByActivity(a1):
            print(s)

        print("Macro Elements for Child " + str(ch1) + ":")
        for s in db.macroElement.getByChild(ch1):
            print(s)

        # print("Navigation steps for schedule item " + str(s3) + ":")
        # for s in db.navigationStep.getByActivity(a1):
        #     print(s)

        # print("Remove children for parent p1")
        # db.child.removeByParent(p1)
        print("Children in class: ")
        for cc in db.getChildrenInClasses():
            print(cc)

        print("Schedule items as Local time")
        for item in db.scheduleItem.getAll():
            print("UTC datetime: " + str(item[1]))
            print("Local datetime: " + str(backend.formatAsString(backend.convertToLocal(backend.formatAsDatetime(item[1])))))

        # try:
        #     print("Adding messagess")
        #     db.message.add('Help me', backend.UTCNow(), ch3, p2, 'child')
        #     time.sleep(1)
        #     db.message.add('No', backend.UTCNow(), ch3, p2, 'parent')
        #     time.sleep(1)
        #     db.message.add('Please', backend.UTCNow(), ch3, p2, 'child')
        #     time.sleep(1)
        #     db.message.add('OK', backend.UTCNow(), ch3, p2, 'parent')
        # except Exception as e:
        #     print(e)
        #     raise
        
        db.close()
