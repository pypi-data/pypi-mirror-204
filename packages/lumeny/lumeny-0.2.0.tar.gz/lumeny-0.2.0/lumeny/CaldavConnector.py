import caldav
import timeit
from typing import List
from ConfigLoader import ConfigLoader
from utils import time_usage
import datetime
import random

# function to connect to caldav client using url and username and password
def connect_caldav(url: str, username: str, password: str) -> caldav.DAVClient:
    return caldav.DAVClient(url, username=username, password=password)

def print_calendars_demo(calendars):
    """
    This example prints the name and URL for every calendar on the list
    """
    if calendars:
        ## Some calendar servers will include all calendars you have
        ## access to in this list, and not only the calendars owned by
        ## this principal.
        print("your principal has %i calendars:" % len(calendars))
        for c in calendars:
            print("    Name: %-36s  URL: %s" % (c.name, c.url))
    else:
        print("your principal has no calendars")

def get_calendars(client: caldav.DAVClient) -> List[caldav.Calendar]:
    principal: caldav.Principal = client.principal()
    calendars: List[caldav.Calendar] = principal.calendars()
    return calendars

def add_event_to_calendar(client: caldav.DAVClient, calendar_name: str, event: caldav.Event) -> None:
    principal: caldav.Principal = client.principal()
    calendars: List[caldav.Calendar] = principal.calendars()
    for calendar in calendars:
        if calendar.name == calendar_name:
            calendar.add_event(event)
            break
    
# get all events from a calendar
def get_events_from_a_calendar(client: caldav.DAVClient, calendar_name: str) -> List[caldav.Event]:
    # use map instead of for loop
    principal: caldav.Principal = client.principal()
    calendars: List[caldav.Calendar] = principal.calendars()
    
    # find the calendar with the given name using for loop
    for calendar in calendars:
        if calendar.name == calendar_name:
            break

    print(f"\033[1;34m{calendar.name}\033[0m")

    return calendar.events()

# store calendar names in config file under caldav section, given calendars
def store_calendar_names_in_config(calendars: List[caldav.Calendar]) -> None:
    config_loader = ConfigLoader()
    config = config_loader.get_config()
    caldav_config = config["caldav"]
    # store calendar names in config
    caldav_config["calendar_names"] = list(map(lambda calendar: calendar.name, calendars))
    # write config
    config_loader.write_config(config)
    print("\033[1;32mSuccessfully stored calendar names in config file\033[0m")

# get calendar names from config file
def get_calendar_names_from_config() -> List[str]:
    config_loader = ConfigLoader()
    config = config_loader.get_config()
    caldav_config = config["caldav"]
    # get calendar names from config
    calendar_names: List[str] = caldav_config["calendar_names"]
    return calendar_names

# write function to print every event from events list
def print_events(events: List[caldav.Event]) -> None:
    # for each event, print event name and start date
    for event in events:
        print(f"{event.instance.vevent.summary.value} {event.instance.vevent.dtstart.value}")

# search for events in all calendars given a time interval
@time_usage
def search_events_by_day(client: caldav.DAVClient, start: datetime.datetime, end: datetime.datetime) -> List[caldav.Event]:

    principal: caldav.Principal = client.principal()
    calendars: List[caldav.Calendar] = principal.calendars()

    overall_events: List[caldav.Event] = []

    for time in [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]:
        # use calendar.search to get events
        for calendar in calendars:
            events: List[caldav.Event] = calendar.search(start=time, end=time + datetime.timedelta(days=1), expand=True, event=True)
            overall_events.extend(events)
    
    
    return overall_events
        
        


def test_connect_caldav():
    
    config_loader = ConfigLoader()
    config = config_loader.get_config()
    caldav_config = config["caldav"]

    client: caldav.DAVClient = connect_caldav(
        caldav_config["url"], caldav_config["username"], caldav_config["password"]
    )
    
    principal: caldav.Principal = client.principal()
    
    calendars: List[caldav.Calendar] = principal.calendars()
    
    # get calendar
    calendar: caldav.Calendar = calendars[0]
    # get today
    today: datetime.datetime = datetime.datetime.today()
    # get all events from today to 30 days from now
    events: List[caldav.Event] = search_events_by_day(client, today, today + datetime.timedelta(days=7))
    print(type(events[0]))
    # print events
    print_events(events)
    
if __name__ == "__main__":
    test_connect_caldav()