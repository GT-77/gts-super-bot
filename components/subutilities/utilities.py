client = None
def utfopen(*args, **args):
    return open(*args, encoding = "UTF-8", **args)
def quickread(filepath):
    with _utfopen(filepath) as file:
        return file.read()
def quickwrite(filepath, writing):
    with _utfopen(filepath, "w") as file:
        return file.write(writing)
def assert_(condition, function, *args, *kwargs):
    """Triggers "function" and raises AssertError if "condition" is false"""
    if not condition:
        function(*args, **kwargs)
        raise AssertError()
def message(*args, **kwargs):
    client.send_message(*args, **kwargs)
