from flask import redirect, render_template, request, session

def apology(message, code=400):
    return render_template("apology.html", err_msg=message), code
