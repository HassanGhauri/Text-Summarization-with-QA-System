import json
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from services.bert import answer_question
from services.helpers import apology
from services.summerizer import summarize

summary_text = ""
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app = Flask(__name__)




# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route('/success', methods = ['POST'])   
def success():   
    if request.method == 'POST':   
        f = request.files['file'] 
        f.save(f.filename)

        file = open(f'{f.filename}', "r")
        input_file = file.read().strip()
        summary = summarize(input_file)
        global summary_text
        x = summary
        summary_text = x
        print(summary_text)
        return redirect('/')   
         


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/more_info")
def about():
    return render_template("more_info.html")

@app.route("/get_answer", methods=["POST"])
def get_answer():
    params = json.loads(request.get_data().decode("utf-8"))
    question = params["question"]
    
    if not question:
        return "Please enter your question"
    
    response = answer_question(question, summary_text)
    return response


@app.route("/get_summary", methods=["POST"])
def get_summary():
    params = json.loads(request.get_data().decode("utf-8"))
    print("params")
    print(params)
    print(summary_text)
    input_text = params["input_text"]
    return summary_text
         

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


if __name__ == "__main__":  
  app.run(debug = True)