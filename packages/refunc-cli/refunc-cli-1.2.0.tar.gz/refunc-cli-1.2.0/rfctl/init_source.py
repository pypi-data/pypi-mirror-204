
python_source = {
    "main.py": """
def lambda_handler(event,ctx):
    return {
        "msg":"hello"
    }""",
    "test.py": """
from rfctl.client import LambdaClient

client = LambdaClient("{namespace}")

rsp = client.invoke_function("{name}", {}, get_log=True)

print(rsp)
""",
    "requirements.txt": """""",
}

sources = {
    "python": python_source
}
