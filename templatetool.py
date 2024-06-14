def getNoBodyCode(path, method):
    # turn method to lower case
    method = method.lower()
    # code template
    code = f'''
import requests

baseUrl = 'your base url'
path = '{path}'
url = baseUrl + path

headers = {{
    'Content-Type': 'application/json'
}}

response = requests.{method}(url, headers=headers)
print(response.text)
    '''
    return code

def getBodyCode(path, method, body):
    # turn method to lower case
    method = method.lower()
    # code template
    code = f'''
import requests

baseUrl = 'your base url'
path = '{path}'
url = baseUrl + path

headers = {{
    'Content-Type': 'application/json'
}}
data = {body}

response = requests.{method}(url, headers=headers, json=data)
print(response.text)
    '''
    return code

def convertDescriptionToPythonCode(path, method, body=None):
    if body is None:
        return getNoBodyCode(path, method)
    else:
        return getBodyCode(path, method, body)