import json
import yaml
from swaggerHandler.EndPoint import EndPoint
from pprint import pprint

class SwaggerFile:
    def __init__(self, filePath, fileType):
        # convert json/yaml file to python object
        data = None
        if fileType == 'json':
            with open(filePath, 'r') as swaggerFile:
                data = json.load(swaggerFile)  
        elif fileType == 'yaml':
            with open(filePath, 'r') as swaggerFile:
                data = yaml.safe_load(swaggerFile)
        else:
            pass

        self.version = ''
        self.basePath = ''
        self.endPoints = []

        # 1. set document version
        if 'swagger' in data:
            self.version = data['swagger']
        elif 'openapi' in data:
            self.version = data['openapi']
        else:
            self.version = ''

        #2. set base path
        if 'basePath' in data:
            self.basePath = data['basePath']
        else:
            self.basePath = ''

        #3. set endpoints
        paths = data['paths'] 
        for path, pathContent in paths.items():
            for method, endPointContent in pathContent.items():
                endPoint = EndPoint(endPointContent,path,method)
                self.endPoints.append(endPoint)