from flask import Flask, render_template, request, jsonify
    # GROQ API REQUEST

    headers = {
        "Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json={
            "model": "llama3-8b-8192",
            "messages": [
                {
                    "role": "system",
                    "content": "You are SRG.ai, an intelligent AI assistant for electronics, coding, Arduino, embedded systems, robotics, PCB design and engineering."
                },
                {
                    "role": "user",
                    "content": prompt
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