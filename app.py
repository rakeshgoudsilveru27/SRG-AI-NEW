from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# UPLOAD FOLDER

UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# CHAT MEMORY

conversation_history = []

# HOME PAGE

@app.route('/')

def home():

    return render_template('index.html')

# CHAT ROUTE

@app.route('/chat', methods=['POST'])

def chat():

    user_message = request.form['message']

    selected_model = request.form['model']

    image = request.files.get('image')

    # SAVE IMAGE

    if image:

        image_path = os.path.join(

            app.config['UPLOAD_FOLDER'],
            image.filename

        )

        image.save(image_path)

    # SAVE USER MESSAGE

    conversation_history.append(

        f"User: {user_message}"

    )

    # FULL HISTORY

    history = "\n".join(conversation_history)

    # AI PROMPT

    prompt = f"""
    You are SRG.ai.

    A smart AI assistant for:

    - Electronics
    - Arduino
    - PCB Design
    - Embedded Systems
    - Robotics
    - Engineering
    - Coding
    - Circuit Analysis
    - Microcontrollers

    Continue the conversation naturally.

    If the user uploaded an image,
    mention that the image was received successfully.

    Conversation History:

    {history}

    Assistant:
    """

    # GROQ API REQUEST

    headers = {

        "Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}",

        "Content-Type": "application/json"
    }

    response = requests.post(

        "https://api.groq.com/openai/v1/chat/completions",

        headers=headers,

        json={

            "model":"llama3-8b-8192",

            "messages":[

                {

                    "role":"system",

                    "content":"You are SRG.ai, an intelligent AI assistant for electronics, coding, Arduino, embedded systems, robotics, PCB design and engineering."

                },

                {

                    "role":"user",

                    "content":prompt

                }

            ]

        }

    )

data = response.json()

print(data)

if "choices" in data:

    ai_reply = data["choices"][0]["message"]["content"]

else:

    ai_reply = f"Groq API Error: {data}"

    # SAVE AI RESPONSE

    conversation_history.append(

        f"Assistant: {ai_reply}"

    )

     # RETURN RESPONSE
    return jsonify({
        'reply': ai_reply

     })
# RUN APP

if __name__ == '__main__':

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    port = int(os.environ.get("PORT", 5000))

    app.run(

        host="0.0.0.0",
        port=port

    )