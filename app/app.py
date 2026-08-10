from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello from my DevOps application!"


@app.route("/health")
def health():
    return jsonify(status="UP")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
