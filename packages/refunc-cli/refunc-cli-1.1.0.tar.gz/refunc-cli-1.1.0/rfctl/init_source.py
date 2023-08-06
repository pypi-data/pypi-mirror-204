
python_source = {
    "main.py": """
def lambda_handler(ctx,event):
    return {
        "msg":"hello"
    }""",
    "requirements.txt": """""",
}

sources = {
    "python": python_source
}
