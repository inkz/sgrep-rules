from flask import make_response

def foo():
    x = requests.args.get("x")
    make_response("found {}".format(x))