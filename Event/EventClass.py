import sys

import redis

from _datetime import datetime


class MyEvent():

    def __init__(self):

        rhost = 'localhost'
        rport = 6379
        self.r = redis.Redis(host=rhost, port=rport, decode_responses=True)

    # 1 record a venue
    def record_a_venue(self, venue):
        if self.r.sismember("s_venues", venue):
            print("venue is already recorded")
        else:
            self.r.sadd("s_venues", venue)

    # 2 record an event
    def record_an_event(self, name, start_time, venue, duration, name_of_responsible_person,
                        phone_of_responsible_person):
        if not self.r.sismember("s_venues", venue):
            print("the venue is not recorded ")
        else:
            self.r.zadd("z_start_times", {start_time: start_time})
            self.r.hmset("h_" + str(start_time) + "_event_details", {"name": name,
                                                                     "start_time": start_time,
                                                                     "venue": venue,
                                                                     "duration": duration,
                                                                     "name_of_responsible_person": name_of_responsible_person,
                                                                     "phone_of_responsible_person": phone_of_responsible_person})

    # 3 list the events in a given time
    def list_events_by_time(self, start_time):
        if self.r.zscore("z_start_times", start_time) is None:
            print("the event time is not exist")
        else:
            print(self.r.hgetall("h_" + str(start_time) + "_event_details"))
            # end_time = start_time + self.r.hget(("h_" + str(start_time) + "_event_details","duration"))
            # print(self.r.hget(("h_" + str(start_time) + "_event_details","duration")))

    # 4
    def list_events_sort_by_time(self):
        start_times = self.r.zrange("z_start_times", 0, -1, True)
        for start_time in start_times:
            print(self.r.hgetall("h_" + str(start_time) + "_event_details"))

    # 5
    def record_ticket_type(self, ticket_type, price, validity_start, validity_end):
        self.r.sadd("s_ticket_types",ticket_type)
        self.r.hmset("h_ticket_type_" + ticket_type, {"ticket_type": ticket_type,
                                                       "price": price,
                                                       "validity_start": validity_start,
                                                       "validity_end": validity_end})

    # 6
    def record_guests_buy_ticket(self,name,birth_date,gender,ticket_type):
        if ticket_type != self.r.hget("h_ticket_type_" + ticket_type,"ticket_type"):
            print("ticket_type is not registered ")
        else:
            self.r.sadd("s_guest_names",name)
            self.r.hmset("h_guest_"+name+"_ticket_details",{"birth_date":birth_date,
                                                            "gender":gender,
                                                            "ticket_type":ticket_type})

    # 7
    def list_guests(self):
        print(self.r.smembers("s_guest_names"))


    # 8


    # 9
    def list_ticket_types(self):
        print(self.r.smembers("s_ticket_types"))