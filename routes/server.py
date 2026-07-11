from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return "SRG AI Server Running"

@app.route("/ping")
def ping():
    return jsonify({
        "status": "online",
        "device": "SRG AI Server",
        "version": "V1.1"
    })

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    message = data["message"].strip().lower()

    print("\n==============================")
    print("Question from ESP32:")
    print(message)
    print("==============================")

    # AI Logic (Temporary)

    if message == "what is ohm's law?":
        answer = "Ohm's Law states that Voltage equals Current multiplied by Resistance."

    elif message == "who are you?":
        answer = "I am SRG AI, your smart glasses assistant."

    elif message == "hello":
        answer = "Hello Rakesh. Nice to see you."

    elif message == "what is your name?":
        answer = "My name is SRG AI."

    else:
        answer = "Sorry, I don't know the answer yet."

    return jsonify({
        "reply": answer
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)