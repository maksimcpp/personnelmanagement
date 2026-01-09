class InvalidTeamId(Exception):
    def __init__(self):
        super().__init__('Invalid team id.')


class InvalidEmployeeId(Exception):
    def __init__(self):
        super().__init__('Invalid employee id.')


class EmployeeNotActive(Exception):
    def __init__(self):
        super().__init__('Employee is not active.')


class EmployeeNotExist(Exception):
    def __init__(self):
        super().__init__('Employee is not exist.')
