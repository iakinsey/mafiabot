class AppException(Exception):
    public = False


class NoSuchQuery(AppException):
    pass


class InsufficientFunds(AppException):
    public = True


class InvalidCommand(AppException):
    public = True
