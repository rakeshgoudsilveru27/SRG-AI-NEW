from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import requests
import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found"
    )
print(
    "GROQ FOUND:",
    bool(GROQ_API_KEY)
)

print(
    "GEMINI FOUND:",
    bool(os.environ.get(
        "GEMINI_API_KEY"
    ))
)
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

GEMINI_API_KEY = os.environ.get(
    "GEMINI_API_KEY"
)

OPENWEATHER_API_KEY = os.environ.get(
    "OPENWEATHER_API_KEY"
)


if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not found")

genai.configure(
    api_key=GEMINI_API_KEY
)

gemini_model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def get_weather(city):

    try:

        url = (
            "https://api.openweathermap.org/data/2.5/weather"
        )

        params = {

            "q": city,

            "appid":
            OPENWEATHER_API_KEY,

            "units":
            "metric"

        }

        response = requests.get(

            url,

            params=params,

            timeout=10

        )

        data = response.json()

        print(data)


        return f"""
🌤 Weather in {city.title()}

🌡 Temperature: {data['main']['temp']}°C

💧 Humidity: {data['main']['humidity']}%

☁ Condition: {data['weather'][0]['description']}
"""

    except Exception as e:

        print(
            "WEATHER ERROR:",
            str(e)
        )

        return f"Weather Error: {str(e)}"
    

def get_tomorrow_weather(city):

    try:

        url = (
            "https://api.openweathermap.org/data/2.5/forecast"
        )

        params = {

            "q": city,

            "appid":
            OPENWEATHER_API_KEY,

            "units":
            "metric"

        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        print(data)

        print(
            data["list"][8]
        )

        tomorrow = data["list"][8]

        return f"""
🌤 Tomorrow Weather in {city.title()}

🌡 Temperature: {tomorrow['main']['temp']}°C

💧 Humidity: {tomorrow['main']['humidity']}%

☁ Condition: {tomorrow['weather'][0]['description']}
"""

    except Exception as e:

        return f"Forecast Error: {str(e)}"    
    
def get_wikipedia_summary(query):

    try:

        search_url = (
            "https://en.wikipedia.org/w/api.php"
        )

        params = {

            "action": "query",

            "list": "search",

            "srsearch": query,

            "format": "json"

        }

        response = requests.get(

            search_url,

            params=params,

            timeout=10

        )

        data = response.json()

        print(data)

        results = data.get(
            "query",
            {}
        ).get(
            "search",
            []
        )
        if not results:

            return None

        page_title = results[0]["title"]

        summary_url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            +
            page_title.replace(
                " ",
                "_"
            )
        )

        summary_response = requests.get(

            summary_url,

            timeout=10

        )

        summary_data = summary_response.json()

        if "extract" in summary_data:

            return f"""
📚 Wikipedia

Title:
{page_title}

Summary:
{summary_data['extract']}
"""

        return None

    except Exception as e:

        print(
            "WIKIPEDIA ERROR:",
            str(e)
        )

        return None    

# UPLOAD FOLDER
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# CHAT MEMORY
conversation_history = []

# HOME PAGE
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/chat", methods=["GET"])
def chat_page():
    return render_template("index.html")
# CHAT ROUTE
@app.route('/chat', methods=['POST'])
def chat():

    user_message = request.form.get(
        'message',
        ''
    ).strip()
    
    image = request.files.get('image')

    if not user_message and not image:

        return jsonify({

            "reply":
            "Please enter a message.",

            "title":
            "New Chat"

        })

    

    # SAVE IMAGE

    prompt_image_text = ""

    if image and image.filename:

        allowed_extensions = [
            "png",
            "jpg",
            "jpeg",
            "webp"
        ]

        if "." not in image.filename:

            return jsonify({

                "reply":"Invalid file.",
                "title":"Image Error"

            })

        ext = image.filename.rsplit(".",1)[1].lower()

        if ext not in allowed_extensions:

            return jsonify({

                "reply":"Invalid image format.",
                "title":"Image Error"

            })

        os.makedirs(
            UPLOAD_FOLDER,
            exist_ok=True
        )

        filename = secure_filename(
            image.filename 
        )

        image_path = os.path.join(
            app.config['UPLOAD_FOLDER'],
            filename
        )

        image.save(image_path)

        print("IMAGE SAVED")

        try:

            img = Image.open(image_path)

            vision_model = genai.GenerativeModel(
                "gemini-2.5-flash"
            )

            vision_response = vision_model.generate_content([
                user_message,
                img
            ])

            print("GEMINI RESPONSE RECEIVED")
            print(vision_response.text)

            ai_reply = vision_response.text

            conversation_history.append(
                f"User: {user_message}"
            )

            conversation_history.append(
                f"Assistant: {ai_reply}"
            )

            conversation_history[:] = conversation_history[-20:]

            return jsonify({

                "reply": ai_reply,

                "title": "Image Analysis"

            })

        except Exception as e:

            print("GEMINI ERROR:", str(e))

            return jsonify({
                "reply": "Image analysis failed.",
                "title": "Image Error"
            })

        prompt_image_text = f"""
        User uploaded image:
        {image.filename}
        """

    # SAVE USER MESSAGE

    conversation_history.append(
        f"User: {user_message}"
    )

    # FULL HISTORY

    history = "\n".join(
        conversation_history
    )

    # AI PROMPT

    prompt = f"""
You are SRG.ai, an advanced AI assistant.

Specializations:
- Embedded Systems
- Electronics
- IoT
- Robotics
- PCB Design
- VLSI
- Programming
- AI & Machine Learning

Rules:
- Give accurate answers.
- Explain step by step.
- For coding, provide complete code.
- For electronics, explain components and wiring.
- If unsure, say so.

Conversation History:

{history}

{prompt_image_text if image else ""}

Assistant:
"""

    # GROQ API HEADERS
        
    headers = {

        "Authorization":
        f"Bearer {GROQ_API_KEY}",

        "Content-Type":
        "application/json"
    }

    # AUTO AI MODEL SELECTION

    message_lower = user_message.lower()

        
    weather_keywords = [

        "weather",
        "wether",
        "waether",

        "temperature",
        "temp",

        "forecast",

        "humidity",

        "rain",

        "hot",
        "cold",

        "climate",

        "sunny",
        "cloudy",
        "windy"
    ]

    is_weather_query = any(

        word in message_lower

        for word in weather_keywords

    )

    city_aliases = {

        "hyd": "hyderabad",
        "hyderabad": "hyderabad",

        "mum": "mumbai",
        "mumbai": "mumbai",

        "del": "delhi",
        "delhi": "delhi",

        "blr": "bangalore",
        "bangalore": "bangalore",

        "chn": "chennai",
        "chennai": "chennai",

        "kol": "kolkata", 
        "kolkata": "kolkata"
    }

    city = None

    for alias, real_city in city_aliases.items():
   
        if alias in message_lower:

            city = real_city

            break

    if not city:

        words = message_lower.split()

        weather_words = [

            "weather",
            "wether",
            "waether",

            "temp",
            "temperature",

            "forecast",

            "humidity",

            "rain",

            "hot",

            "cold"
        ]

        skip_words = [

            "how",
            "what",
            "is",
            "the",
            "in",
            "for",
            "will",
            "it",
            "be",
            "today",
            "tomorrow",
            "please",
            "show" 
        ]

        for word in words:

            if (
                word not in weather_words
                and
                word not in skip_words
                and
                len(word) > 2
            ):

                city = word

                break

    date_type = "today"

    if "tomorrow" in message_lower:
  
        date_type = "tomorrow"

    elif "today" in message_lower:

        date_type = "today"  


    print("QUERY =", message_lower)
    print("CITY =", city)
    print("DATE =", date_type)

    
    
    if is_weather_query and city:

        if date_type == "tomorrow":

            return jsonify({

                "reply":
                 get_tomorrow_weather(city),

                "title":
                f"Tomorrow Weather {city}"

            })

        return jsonify({

            "reply":
            get_weather(city),

            "title":
            f"Weather {city}"

        })

    if len(user_message) > 200:

        selected_model = "llama-3.1-8b-instant"

    elif any(word in message_lower for word in [

        "project",
        "architecture",
        "flask",
        "python",
        "robot",
        "embedded",
        "system design",
        "database",
        "machine learning",
        "dsa",
        "algorithm"

    ]):

        selected_model = "llama-3.3-70b-versatile"

    else:

        selected_model = "llama-3.3-70b-versatile"

    # MAIN AI RESPONSE

    try:
        gemini_response = gemini_model.generate_content(
            prompt
        )

        if hasattr(gemini_response, "text"):
            ai_reply = gemini_response.text
        else:
            ai_reply = "No response generated."

        chat_title = user_message[:30]

    except Exception as e:
 
        print("GEMINI FAILED:", str(e))
        print("SWITCHING TO GROQ")

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json={
                "model": selected_model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are SRG.ai."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=60
        )

        if response.status_code != 200:
            return jsonify({
                "reply": "AI service unavailable.",
                "title": "Error"
            })

        data = response.json()

        ai_reply = data["choices"][0]["message"]["content"]

        chat_title = user_message[:30]


    # SAVE AI RESPONSE

    conversation_history.append(
        f"Assistant: {ai_reply}"
    )

    # LIMIT MEMORY

    conversation_history[:] = (
        conversation_history[-20:]
    )

    # RETURN RESPONSE

    return jsonify({

        'reply': ai_reply,

        'title': chat_title,
    })

@app.route('/new-chat', methods=['POST'])
def new_chat():

    global conversation_history

    conversation_history = []

    print("CHAT MEMORY CLEARED")

    return jsonify({
        "status":"success"
    })

# RUN APP



if __name__ == '__main__':

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )