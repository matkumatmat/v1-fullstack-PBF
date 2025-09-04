class ValidationError(Exception):
    """Custom exception for validation errors in the service layer."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
