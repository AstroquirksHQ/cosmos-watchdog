class EmptyResponseException(Exception):
    def __init__(self, url):
        self.url = url
        super().__init__()

    def __repr__(self):
        return f"EmptyResponseException: {self.url}"
