from MyHelpdeskClass import Helpdesk

rf = Helpdesk()

# rf.setNewEmployee("email1")
# rf.setNewEmployee("email2")
# rf.setNewEmployee("email3")
#
# #rf.deleteEmployee("email2")
# rf.listAllEmployees()
#
# rf.set_manager("email1")
# rf.get_manager()
#
# rf.set_new_task("email1","new_task-1","we need to do sth1")
# rf.set_new_task("email1","new_task-2","we need to do sth2")
#rf.set_new_task("email1","new_task-4","we need to do sth4")

# rf.get_task_details(2)
# rf.set_priority("email1",2,10)
# rf.get_priority(2)
#rf.set_employee_to_work(2,"email1","email2")
rf.perform_task("email1",2)