from flask import Flask, render_template, request
from flask_cors import CORS
from command_interpreter import CommandInterpreter

app = Flask(__name__)
cors = CORS(app)

@app.route("/",methods=['GET','OPTIONS'])
def home():
    ci = CommandInterpreter()
    data = request.args.get("command")
    ci.interpreter(data)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
