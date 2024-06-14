from zhipuai import ZhipuAI
import os

def convertDescriptionToPythonCode(description):
    # init the zhipuAI client
    key = os.environ.get('ZHIPUAI_APIKEY')
    client = ZhipuAI(api_key = key)

    prompt = f'''
    请将根据下面对一个http request的描述，将其转换为使用python requests库发送请求的代码。
    {description}
    结果中请不要包含除了代码的任何其余信息。
    请求的baseurl用一个参数代替。
    headers里面填充常见的header即可。
    '''

    _messages = []
    _messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model = "glm-4",
        messages = _messages
    )
    return response.choices[0].message.content