from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

@app.route("/",methods=['GET','OPTIONS'])
def home():
    data = request.args.get("command")
    print(data)
    return ""
    
if __name__ == "__main__":
    app.run(debug=True)
