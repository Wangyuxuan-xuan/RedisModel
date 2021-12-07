import sys

import redis

from _datetime import datetime


class MyTaxi():

    def __init__(self):

        rhost = 'localhost'
        rport = 6379
        self.r = redis.Redis(host=rhost, port=rport, decode_responses=True)

    # 1
    def set_new_taxi(self, license_plate, driver_name, number_of_transportable_passengers, production_year_of_car,
                     car_type, phone_number):
        self.r.sadd("s_taxi_license_plates", license_plate)
        self.r.hmset("h_taxi_" + license_plate + "_details", {"driver_name": driver_name,
                                                              "number_of_transportable_passengers": number_of_transportable_passengers,
                                                              "production_year_of_car": production_year_of_car,
                                                              "car_type": car_type,
                                                              "phone_number": phone_number})

    # 10
    def get_taxi_details_by_license_plate(self, license_plate):
        if not self.r.sismember("s_taxi_license_plates", license_plate):
            print("The " + license_plate + " is not a taxi")
        else:
            print("taxi_details :")
            print(self.r.hgetall("h_taxi_" + license_plate + "_details"))

    # 13
    def get_all_cars(self):
        print("list of all cars :")
        print(self.r.smembers("s_taxi_license_plates"))

    # 2

    def set_begin_to_work(self, license_plate, from_date_time):
        if not self.r.sismember("s_taxi_license_plates", license_plate):
            print("The taxi is not exists")
            sys.exit()
        if self.r.zscore("z_working_taxis", license_plate) is not None:
            print("The taxi is already at work")
            sys.exit()
        else:
            self.r.zadd("z_working_taxis", {license_plate: from_date_time})
            self.r.zadd("z_taxi_" + license_plate + "_working_time_recorder", {"from_date_time": from_date_time})

    # 4
    def get_working_taxis(self):
        print("working_taxis :")
        print(self.r.zrange("z_working_taxis", 0, -1, True, True))

    # 3
    def set_finish_work(self, license_plate, to_date_time):
        if not self.r.sismember("s_taxi_license_plates", license_plate):
            print("The taxi is not exists")
            sys.exit()
        if self.r.zscore("z_working_taxis", license_plate) is None:
            print("The taxi is not at work")
            sys.exit()
        else:
            self.r.zadd("z_taxi_finish_work", {license_plate: to_date_time})
            self.r.zadd("z_taxi_" + license_plate + "_working_time_recorder", {"to_date_time": to_date_time})
            period = self.r.zscore("z_taxi_" + license_plate + "_working_time_recorder",
                                   "to_date_time") - self.r.zscore("z_taxi_" + license_plate + "_working_time_recorder",
                                                                   "from_date_time")
            self.r.zadd("taxi_working_time_period", {license_plate: period})
            self.r.zrem("z_working_taxis", license_plate)

    def get_finish_work_taxis(self):
        print("finish_work_taxis :")
        print(self.r.zrange("z_taxi_finish_work", 0, -1, True, True))

    # 5
    def set_new_route_order(self, address_from, address_to, date_time_from, number_of_passengers):
        route_id = self.r.incr("route_id")
        self.r.sadd("current_route_ids", route_id)
        self.r.hmset("h_route_order_" + str(route_id), {"address_from": address_from,
                                                        "address_to": address_to,
                                                        "date_time_from": date_time_from,
                                                        "number_of_passengers": number_of_passengers})

    # 15
    def get_route_order_details_by_route_id(self, route_id):
        print("route_order_details :")
        print(self.r.hgetall("h_route_order_" + str(route_id)))

    # 6
    def set_taxi_to_route(self, license_plate, route_id):
        if not self.r.sismember("s_taxi_license_plates", license_plate):
            print("The taxi is not exists")
            sys.exit()
        if self.r.zscore("z_working_taxis", license_plate) is None:
            print("The taxi is not at work")
            sys.exit()
        if not self.r.exists("h_route_order_" + str(route_id)):
            print("route not exist")
            sys.exit()
        if self.r.sismember("taxi_having_route", license_plate):
            print("taxi already has a route")
            sys.exit()
        if self.r.sismember("route_ongoing", route_id):
            print("route is already assigned")
            sys.exit()
        else:
            self.r.sadd("taxi_having_route", license_plate)
            self.r.sadd("route_ongoing", route_id)
            self.r.hset("taxi_" + license_plate + "having_route", "route_id", route_id)
            self.r.hset("taxi_" + str(route_id) + "having_route", "license_plate", license_plate)

    # 14. list of the assigned and not fullfilled routes
    def get_taxi_and_assigned_routes(self):
        license_plates = self.r.smembers("taxi_having_route")
        for license_plate in license_plates:
            print("license_plate :" + license_plate + " assigned on route : ")
            print(self.r.hgetall("taxi_" + license_plate + "having_route"))

    # 11. list of the ordered and not assigned routes
    def get_ordered_but_not_assigned_routes(self):
        route_ids = self.r.smembers("current_route_ids")
        for route_id in route_ids:
            if not self.r.sismember("route_ongoing", route_id):
                print("ordered_but_not_assigned_routes :")
                print("route_id : " + route_id)
                self.get_route_order_details_by_route_id(route_id)

    def get_assigned_routes(self):
        route_ids = self.r.smembers("route_ongoing")
        for route_id in route_ids:
            print("assigned_routes :")
            print("route_id : " + route_id)
            self.get_route_order_details_by_route_id(route_id)

    # 7 fulfill a route, record the price and distance, date_time_to
    def set_fulfill_route(self, route_id, price, distance, date_time_to):
        if self.r.sismember("fulfilled_route_ids", route_id):
            print("route is already fulfilled !")
            sys.exit()
        if not self.r.sismember("route_ongoing", route_id):
            print("route is not assigned , can not be fulfilled !")
            sys.exit()
        else:

            self.r.sadd("fulfilled_route_ids", route_id)
            self.r.hmset("h_route_order_" + str(route_id), {"price": price,
                                                            "distance": distance,
                                                            "date_time_to": date_time_to})
            license_plate = self.r.hget("taxi_" + str(route_id) + "having_route", "license_plate")
            self.r.srem("route_ongoing",route_id)
            self.r.srem("taxi_having_route",license_plate)
            self.r.zincrby("car_distance", distance, license_plate)

    def get_fulfilled_routes(self):
        route_ids = self.r.smembers("fulfilled_route_ids")
        for route_id in route_ids:
            print("fulfilled_route_id :")
            print("route_id : " + route_id)
            self.get_route_order_details_by_route_id(route_id)

    # 8. list of cars and drivers with from_date_time of the work and period of that work.
    # The list should be descending sorted by the period
    def get_taxi_work_time(self, license_plate):
        print(self.r.zrange("taxi_working_time_period", 0, -1, True, True))
        print(license_plate + "from_date_time : ")
        print(self.r.zscore("z_taxi_" + license_plate + "_working_time_recorder", "from_date_time"))

    # 9. list of cars and drivers sorted by the sum of distances
    def get_taxi_by_the_sum_of_distances(self):
        print(self.r.zrange("car_distance", 0, -1, True, True))
