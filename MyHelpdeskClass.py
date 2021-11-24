import redis

class Helpdesk():

    def __init__(self):
        
        rhost='localhost'
        rport=6379
        self.r=redis.Redis(host=rhost, port=rport,decode_responses=True)

    #1   
    def setNewEmployee(self,email):
        self.r.sadd("set_employees",email)

    #2
    def deleteEmployee(self,email):
        self.r.srem("set_employees",email)

    #3 
    def listAllEmployees(self):
        print(self.r.smembers("set_employees"))

    #4
    def set_manager(self,email):
        if not (self.r.sismember("set_employees",email)):
            print("He / She is not an employee !")
        else:
            self.r.set("manager",email)

    #5
    def get_manager(self):
        print(self.r.get("manager"))