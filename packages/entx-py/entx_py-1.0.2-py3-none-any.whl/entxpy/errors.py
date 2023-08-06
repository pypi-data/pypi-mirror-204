class InvalidPath(Exception):
    """
    Exception raised if the file path provided does not lead to a valid file.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        
class InvalidOperation(Exception):
    """
    Exception raised if operation is being performed on an incorrect file.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
