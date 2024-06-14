from scapy.all import rdpcap
from scapy.layers.http import *
import json
from swaggerHandler.SwaggerFile import SwaggerFile
import zhipuaitool
import templatetool

swaggerFilePath = 'E:\\y1\\api test\\code\\mycode\\restfuzzgpt\\benchmark\\docs\\openapi-blog.json'
pcapFilePath = 'E:\\y1\\api test\\code\\mycode\\finetune-data-collect\\data\\requests-evomaster-blog.pcap'
outputFilePath = 'E:\\y1\\api test\\code\\mycode\\finetune-data-collect\\output\\blog-finetune-data-template.json'
data = []

# compile swagger file
swagger = SwaggerFile(swaggerFilePath, 'json')
with open (swaggerFilePath, 'r') as f:
    swaggerContent = f.read()

# build a dict to get operationId by method and path
print("building the dict to get operationId by method and path...")
endpoints = swagger.endPoints
endpointDict = {}
for endpoint in endpoints:
    identifier = endpoint.httpMethod + " " + swagger.basePath + endpoint.path
    endpointDict[identifier] = endpoint.operationId
print("build the dict successfully")

# read pcap file
print("reading pcap file...")
packets = rdpcap(pcapFilePath)
print(len(packets))
print("read pcap file successfully")


# check packet one by one
idx = 0
last_idx = len(packets) - 1
while idx <= last_idx:
    packet = packets[idx]
    if 'HTTPRequest' in packet:
        print(f"-----recoginize a http request. handling {idx} of {last_idx}...-----")
        httpRequest = packet['HTTPRequest']

        # http request: get operation Id by method and path
        preHalf = httpRequest.Path.decode('utf-8').split('?')[0]
        pathElements = preHalf.split('/')
        if pathElements[-1][-1].isdigit():
            pathElements[-1] = '{id}'
        path = '/'.join(pathElements)
        operationId = endpointDict[httpRequest.Method.decode('utf-8').lower() + ' ' + path]
        print("get operationId: ", operationId)

        # judge if the http request has body
        bodyDescription = "the request has no data in body"
        hasBody = False
        if httpRequest.Content_Length is not None and httpRequest.Content_Length != b'0':
            hasBody = True
            bodyRequest = packets[idx + 1]
            bodyDescription = bodyRequest.load.decode('utf-8')
            print("body: ", bodyDescription)
            idx += 1
        
        # bulid http request description
        description = f'''
        httpMethod: {httpRequest.Method.decode('utf-8')}
        path: {httpRequest.Path.decode('utf-8')}
        body: {bodyDescription}
        '''

        # # Method1: turn http request description to python request code with LLM
        # print("turning description to python code using LLM...")
        # code = zhipuaitool.convertDescriptionToPythonCode(description)
        # print("turning description to python code successfully")

        # Method2: turn http request description to python request code with template
        print("turning description to python code using template...")
        code = templatetool.convertDescriptionToPythonCode(httpRequest.Path.decode('utf-8'), httpRequest.Method.decode('utf-8'), body=bodyDescription if hasBody else None)
        print(code)
        print("turning description to python code successfully")

        # construct the one record
        inputStr = f'Below is the swagger/openapi file: \n{swaggerContent}\n\nplease generate a test case for the operation with the operationId "{operationId}"\n'
        record = {"instruction": "please generate a test case for the target endpoint in the following swagger/openapi file",
                  "input": inputStr,
                  "output": code}
        data.append(record)

        print("----------process successfully!----------")
    idx += 1
print("total requests: ", len(data))
# write the data to output file
jsonStr = json.dumps(data, indent=4)
with open(outputFilePath, 'w') as file:
    print("write to file...")
    file.write(jsonStr)
    print("write to file successfully")
