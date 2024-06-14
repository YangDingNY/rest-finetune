class EndPoint:
    def __init__(self, endPointContent, path, method) -> None:
        # basic info
        self.operationId = endPointContent['operationId']
        self.path = path
        self.httpMethod = method
        self.summary = endPointContent['summary'] if 'summary' in endPointContent else ''
        
        # parameters
        self.parameters = []