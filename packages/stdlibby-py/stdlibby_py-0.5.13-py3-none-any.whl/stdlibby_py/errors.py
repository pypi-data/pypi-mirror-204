import sys

class BaseError(Exception):
    def __init__(self, error_code: int=255):
        self.error_code = self.validate_error_code(error_code)

    def raise_cli(self)->None:
        print(self.error_code)
        sys.exit(self.error_code)

    def validate_error_code(self, ec):
        if ec <= 255:
            return ec
        else:
            return 255


class ClyError(BaseError):
    def __init__(self, mesg: str):
        self.mesg = mesg

