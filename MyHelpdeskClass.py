import sys

import redis

from _datetime import datetime


class Helpdesk():

    def __init__(self):

        rhost = 'localhost'
        rport = 6379
        self.r = redis.Redis(host=rhost, port=rport, decode_responses=True)

    # 1
    def setNewEmployee(self, email):
        self.r.sadd("set_employees", email)

    # 2
    def deleteEmployee(self, email):
        self.r.srem("set_employees", email)

    # 3
    def listAllEmployees(self):
        print(self.r.smembers("set_employees"))

    # 4
    def set_manager(self, email):
        if not (self.r.sismember("set_employees", email)):
            print("He / She is not an employee !")
        else:
            self.r.set("manager", email)

    # 5
    def get_manager(self):
        print(self.r.get("manager"))

    # 6
    def set_new_task(self, email, task_name, description):
        if not (self.r.sismember("set_employees", email)):
            print("not an employee !")
        else:
            task_id = self.r.incr("task_id")
            self.r.hmset("h_task_details_" + str(task_id),
                         {"email": email,
                          "task_name": task_name,
                          "description": description})

            dict = {}
            dict[task_id] = 0
            self.r.zadd("zset_task_priority", dict)
            time_now = datetime.now().strftime("%Y%m%d%H%M%S")
            # dict = {}
            # dict[task_id] = time_now
            self.r.zadd("zset_task_recorded_time", {task_id: time_now})  ##Just need to create a dictionary!

    # 7
    def get_task_details(self, task_id):
        print(self.r.hgetall("h_task_details_" + str(task_id)))

    # 8
    def set_priority(self, email, task_id, priority):
        if self.r.get("manager") != email:
            print("Not a manager ! Only manager can change priority !")
        else:
            dict = {task_id: priority}
            self.r.zadd("zset_task_priority", dict)

    def get_priority(self, task_id):
        if self.r.zscore("zset_task_priority", task_id) is None:
            print("task does not exist !")
        else:
            # print("task " + str(task_id) + " : " + self.r.zscore("zset_task_priority", task_id))
            print(self.r.zscore("zset_task_priority", task_id))

    # 9
    def set_employee_to_work(self, task_id, assigner_email, assigned_email):
        if not (self.r.sismember("set_employees", assigner_email)):
            print("assigner_email not belong to an employee !")
            sys.exit()
        if not (self.r.sismember("set_employees", assigned_email)):
            print("assigned_email not belong to an employee !")
            sys.exit()
        if self.r.zscore("zset_task_priority", task_id) is None:
            print("task does not exist !")

        self.r.hmset("h_task_details_" + str(task_id),
                     {"task_id": task_id,
                      "assigner_email": assigner_email,
                      "assigned_email": assigned_email})
        # remember to use hmset
        print(self.r.hgetall("h_task_details_" + str(task_id)))

    # 10
    def perform_task(self, email, task_id):
        print(self.r.hgetall("h_task_details_" + str(task_id)))
        print(self.r.zscore("zset_task_recorded_time", task_id))
        self.get_priority(task_id)
        self.get_manager()
        self.get_perform_task_time()
        # performer email
        print(email)

    def get_perform_task_time(self):
        print(datetime.now().strftime("%Y%m%d%H%M%S"))
