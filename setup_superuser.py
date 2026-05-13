from case_manager.models import SystemUser

user = SystemUser(username="andrew")
user.set_password("2127")
user.role = "admin"
user.save()