from pprint import pprint
from Google import Create_Service
import time
import datetime
import json
import pandas as pd
import pickle
import os


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt

#-----------------------------------------------------------------------------------------------------------------------

def listCals(service):
    """
    list user calendars, returns the service instance

    Parameters
    ----------
    service : NoneType

    """
    return service.calendarList().list().execute()

#-----------------------------------------------------------------------------------------------------------------------

def insertCal(service, calName):
    """
    Creates a calendar, returns a service instance

    Parameters
    ----------
    calName : string
    service : NoneType
    """

    request_body = {
    'summary': calName
    }

    return service.calendars().insert(body=request_body).execute()

#----------------------------------------------------------------------------------------------------------------------    

def deleteCal(service, calId):

    service.calendars().delete(calendarId='c_0i1e05l7vgkd7loul6io8a7ltk@group.calendar.google.com').execute()

#----------------------------------------------------------------------------------------------------------------------

def createEvent(service, calId):

    """
    title = input("Enter event title: ")
    location = input("Enter location/link: ")
    description = input("Enter event description: ")
    year = input("Enter event year, double digit format (ex. 2021): ")
    month = input("Enter numerical month: ")
    day = input("Enter numerical day: ")
    hourStart = input("Enter start time, hour (military format): ")
    minuteStart = input("Enter start time, minute: ")
    hourEnd = input("Enter end time, hour (military format: ")
    minuteEnd = input("Enter end time, minute: ")
    """

    event_request_body = {
        'summary': 'Art Class', #title
        'location': 'https://www.cs.odu.edu/~cpi/old/410/orangf20/', #location
        'description': 'We\'re going to paint buses!', #description
        'colorId': 5,
        'status': 'confirmed',
        'transparency': 'opaque',
        'visibility': 'default',
        'start': {
            'dateTime': convert_to_RFC_datetime(2021, 2, 22, 18, 30), #year, month, day, hourStart, minuteStart
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': convert_to_RFC_datetime(2021, 2, 22, 20, 00), #year, month, day, hourEnd, minuteEnd
            'timeZone': 'America/New_York',
        },       
        'reminders': {
            'useDefault': True,
            #'overrides': [
            #{'method': 'email', 'minutes': 60},
            #{'method': 'popup', 'minutes': 10},
            #],
        },
    }

    maxAttendees = 25
    sendNotifications = True
    sendUpdates = 'none'

    response = service.events().insert(
        calendarId=calId,
        body=event_request_body,
        maxAttendees=maxAttendees,
        sendNotifications = sendNotifications,
        sendUpdates=sendUpdates
        ).execute()
    return response['id']
    


    #eventID = response['id']

def updateEventTime(service, calId, eventId):

    event = service.events().get(calendarId=calId, eventId=eventId).execute()

    event['start'] = {
            'dateTime': convert_to_RFC_datetime(2021, 2, 22, 20, 15),
            'timeZone': 'America/New_York'
            }        
         
    event['end'] = {
            'dateTime': convert_to_RFC_datetime(2021, 2, 22, 22, 00),
            'timeZone': 'America/New_York'
            }
    event['colorId'] = 1      
    
    return service.events().update(calendarId=calId, eventId=eventId, body=event).execute()

#--------------------------------------------------------------------------------------------------------------

def updateLocation(service, calId, eventId):

    event = service.events().get(calendarId=calId, eventId=eventId).execute()

    event['location'] = 'https://www.odu.edu/compsci'
    event['colorId'] = 11

    return service.events().update(calendarId=calId, eventId=eventId, body=event).execute()

#-------------------------------------------------------------------------------------------------------------


def main():

    CLIENT_SECRET_FILE = 'teacher_credentials.json'
    API_NAME = 'calendar'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    calId = 'classroom103808267631022910657@group.calendar.google.com'
    students = ['ball.o.fur2021@gmail.com', 'rostenkow.moo@gmail.com', 'cinna.koo@gmail.com']
    eventId= '958jj9tap1h95r08etnhprp6hk' # to initialize, eventId = createEvent()['id']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    
    eventId = createEvent(service, calId)
    time.sleep(10)
    response = updateEventTime(service, calId, eventId)
    pprint(response)
    time.sleep(20)
    response = updateLocation(service, calId, eventId)
    pprint(response)


if __name__=='__main__':
    main()