class UserAlreadyExist(Exception):
    def __init__(self):
        super().__init__("User with this username/email already exist.")


class UserNotExist(Exception):
    def __init__(self):
        super().__init__("User not exist.")

    
class UserNotAdmin(Exception):
    def __init__(self):
        super().__init__("User is not a admin.")
