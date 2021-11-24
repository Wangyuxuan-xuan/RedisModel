from MyHelpdeskClass import Helpdesk

rf = Helpdesk()

rf.setNewEmployee("email1")
rf.setNewEmployee("email2")
rf.setNewEmployee("email3")

#rf.deleteEmployee("email2")
rf.listAllEmployees()

rf.set_manager("email1")
rf.get_manager()
