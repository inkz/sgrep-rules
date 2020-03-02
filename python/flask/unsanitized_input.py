from flask import make_response

def foo():
    x = request.args.get("x")
    make_response("found {}".format(x))