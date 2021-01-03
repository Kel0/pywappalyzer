class NoArgsException(ValueError):
    def __init__(self, message: str):
        super().__init__()
        self.message = message
