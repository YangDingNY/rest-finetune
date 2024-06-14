from zhipuaitool import convertDescriptionToPythonCode
import json

# description1 = '''
#         httpMethod: PUT
#         path: /wh/warehouses
#         body: {"description":"_EM_0_XYZ_"}
# '''

list1 = [
    {"role": "user", "content": "hello"},
    {"role": "assistant", "content": "end"},
    {"role": "user", "content": "USER: {\"code\": 200, \"message\": \"success\"}"}
]

with open("E:\\y1\\api test\\code\\mycode\\finetune-data-collect\\output\\test.json", "w") as file:
    file.write(json.dumps(list1, indent=4))