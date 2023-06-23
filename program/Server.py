class Server:
    def __init__(self, protocol: str = "https", domain: str = "gdcheerios.com", port: str = None):
        self.protocol = protocol
        self.domain = domain
        self.port = port
        self.url = f"{self.protocol}://{self.domain}{f':{self.port}' if self.port else ''}"
