from MyTaxiClass import MyTaxi
from _datetime import datetime

rf = MyTaxi()

#rf.set_new_taxi("plate_1","name1",1,2010,"type_1",123456)
# rf.set_new_taxi("plate_2","name2",2,2010,"type_2",123456)
# rf.set_new_taxi("plate_3","name3",3,2010,"type_3",123456)
# rf.set_new_taxi("plate_7","name5",5,2010,"type_5",123456)
# rf.get_taxi_details_by_license_plate("plate_3")

time_now = datetime.now().strftime("%Y%m%d%H%M%S")

#rf.set_begin_to_work("plate_1",time_now)
#rf.set_begin_to_work("plate_2",time_now)
#rf.set_begin_to_work("plate_3",time_now)
# rf.set_begin_to_work("plate_7",time_now)
#rf.get_working_taxis()
# rf.set_finish_work("plate_5",time_now)
# rf.get_finish_work_taxis()
# rf.get_working_taxis()
# rf.set_new_route_order("addr_from","addr_to",time_now,3)
# rf.get_route_order_details_by_route_id(1)
# rf.get_all_cars()
# rf.set_taxi_to_route("plate_7",12)
# rf.get_taxi_and_assigned_routes()
# rf.get_ordered_but_not_assigned_routes()
# rf.get_assigned_routes()
# rf.set_fulfill_route(12,100,123,time_now)
# rf.get_fulfilled_routes()
# rf.get_taxi_work_time("plate_7")
#rf.get_taxi_by_the_sum_of_distances()