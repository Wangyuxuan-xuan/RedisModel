# -*- coding: windows-1250 -*-
# for hungarian letter, like �

import redis
from _datetime import datetime
import pdb


class HDClass():

    def __init__(self):

        rhost = 'localhost'
        rport = 6379
        self.r = redis.Redis(host=rhost, port=rport, decode_responses=True)

    def new_emp(self, email):
        self.r.sadd('s_emp', email)

    def del_emp(self, email):
        self.r.srem('s_emp', email)

    def list_emp(self):
        print(self.r.smembers('s_emp'))

    def choose_manager(self, email):  # manager is unique , so using String here
        if not (self.r.sismember('s_emp', email)):
            print('He/she is not an employee')
        else:
            self.r.set('st_manager', email)

    def who_is_manager(self):
        return self.r.get('st_manager')

    # 6
    def new_task(self, email, task_name, description):
        if not (self.r.sismember('s_emp', email)):
            print('no such employee')
        else:
            t_id = self.r.incr('st_task_id')
            # Increments the number stored at key by one.
            # If the key does not exist, it is set to 0 before performing the operation.
            self.r.hmset('h_' + str(t_id),
                         {'email': email,
                          'task_name': task_name,
                          'description': description})
            self.r.zadd('z_task_by_priority', t_id, 0)
            # zadd add key and score
            # when incr , we incr the score , searching by key
            v_time = datetime.now().strftime("%Y%m%d%H%M%S")
            self.r.zadd('z_task_by_time', t_id, v_time)

    # 7
    def task_details(self, task_id):
        print(self.r.hgetall('h_' + str(task_id)))
        print("priority" + self.r.zscore('z_task_by_priority', task_id))
        print("time" + self.r.zscore('z_task_by_time', task_id))

    # 11
    def task_list_by_recording_times(self):
        print(self.r.zrange('z_task_by_time', 0, -1, withscores=True))

    # 12
    def task_list_by_priority(self):
        print(self.r.zrange('z_task_by_priority', 0, -1, withscores=True))

    # 14
    def newest_task_id(self):
        print(self.r.get('st_task_id'))

    # 15
    def task_priority(self, task_id):
        print(self.r.zscore('z_task_by_priority', task_id))

    # 8
    def change_priority(self, email, task_id, priority):
        if self.r.get('st_manager') != email:
            print('He/she is not the manager')
        else:
            if self.r.zscore('z_task_by_priority', task_id) != None:
                self.r.zadd('z_task_by_priority', task_id, priority)
                # If a specified member is already a member of the sorted set,
                # the score is updated 
                # and the element reinserted at the right position 
                # to ensure the correct ordering.
                assigned_email = self.r.hget('h_' + str(task_id), 'assigned_email')
                if assigned_email != None:
                    self.r.zadd('z_' + assigned_email + '_task',
                                task_id, priority)
            else:
                print('wrong task_id')

    # 9
    def assign_employe_to_task(self, task_id,
                               assigner_email,
                               assigned_email):
        if not (self.r.exists('h_' + str(task_id))):
            print('No such task')
            return -1
        if not (self.r.sismember('s_emp', assigner_email)):
            print('No such assigner emp')
            return -1
        if not (self.r.sismember('s_emp', assigned_email)):
            print('No such assigned emp')
            return -1

        self.r.hmset('h_' + str(task_id),
                     {'assigner_email': assigner_email,
                      'assigned_email': assigned_email})

        priority = self.r.zscore('z_task_by_priority', task_id)
        self.r.zadd('z_' + assigned_email + '_task',
                    task_id, priority)

    # 13
    def list_emloyees_tasks(self, email):
        print(self.r.zrevrange('z_' + email + '_task', 0, -1, withscores=True))

    # Apart from the reversed ordering,
    # ZREVRANGE is similar to ZRANGE.

    # As per Redis 6.2.0, this command is considered deprecated.
    # Please prefer using the ZRANGE command 
    # with the REV argument in new code.

    # 10
    def perform_task(self, email, task_id):
        print(task_id)
        print(self.task_details(task_id))
        print(email)
        print(self.r.get('st_manager'))
        print(datetime.now().strftime("%Y%m%d%H%M%S"))

        assigned_email = self.r.hget('h_' + str(task_id), 'assigned_email')
        if assigned_email != None:
            self.r.zrem('z_' + assigned_email + '_task', task_id)
        ##why has to be not null????
        # because some task hasn't assigned

        self.r.delete('h_' + str(task_id))

        self.r.zrem('z_task_by_priority', task_id)
        self.r.zrem('z_task_by_time', task_id)
