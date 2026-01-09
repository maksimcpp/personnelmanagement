class TokenLifetimeExpired(Exception):
    def __init__(self):
        super().__init__("The refresh token's lifetime has expired.")


class TokenNotExist(Exception):
    def __init__(self):
        super().__init__('Token not exist.')


class InvalidUsername(Exception):
    def __init__(self):
        super().__init__("Invalid username.")


class InvalidPassword(Exception):
    def __init__(self):
        super().__init__("Invalid password.")
