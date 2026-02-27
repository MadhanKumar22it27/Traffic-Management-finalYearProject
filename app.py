from flask import Flask, render_template, jsonify
import controller

app = Flask(__name__)

controller.start_controller()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    return jsonify(controller.current_state)

if __name__ == "__main__":
    app.run(debug=True)