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

print(
    "CURRENTS FOUND:",
    bool(os.environ.get(
        "CURRENTS_API_KEY"
    ))
)

print(
    "GNEWS FOUND:",
    bool(os.environ.get(
        "GNEWS_API_KEY"
    ))
)

print(
    "NEWSAPI FOUND:",
    bool(os.environ.get(
        "NEWS_API_KEY"
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

CURRENTS_API_KEY = os.environ.get(
    "CURRENTS_API_KEY"
)

GNEWS_API_KEY = os.environ.get(
    "GNEWS_API_KEY"
)

NEWS_API_KEY = os.environ.get(
    "NEWS_API_KEY"
)


if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not found")

genai.configure(
    api_key=GEMINI_API_KEY
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

def get_currents_news():

    try:

        url = (
            "https://api.currentsapi.services/v1/latest-news"
        )

        params = {

            "apiKey":
            CURRENTS_API_KEY

        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        articles = data["news"][:5]

        result = "📰 Latest News\n\n"

        for i, article in enumerate(
            articles,
            start=1
        ):

            result += (
                f"{i}. "
                f"{article['title']}\n\n"
            )

        return result

    except Exception as e:

        return (
            f"News Error: {str(e)}"
        )
    
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
You are SRG.ai.

A smart, intelligent and helpful AI assistant.

You can help with:
- Technology
- Programming
- Electronics
- Science
- Mathematics
- Education
- Career Guidance
- Business
- History
- Geography
- General Knowledge
- Daily Life Questions
- Productivity
- AI and Machine Learning
- Robotics
- Embedded Systems

Continue the conversation naturally.

Continue the conversation naturally.

If the user uploaded an image,
mention that the image was received successfully.

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
    if message_lower == "news":

        return jsonify({

            "reply":
            get_currents_news(),

            "title":
            "Latest News"

        })

        
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

        selected_model = "llama-3.3-70b-versatile"

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

        selected_model = "llama-3.1-8b-instant"

    # MAIN AI RESPONSE

    response = requests.post(

        "https://api.groq.com/openai/v1/chat/completions",

        headers=headers,

        json={

            "model": selected_model,

            "messages": [

                {
                    "role": "system",

                    "content":
                    """
You are SRG.ai, a powerful, intelligent and friendly AI assistant.

You can answer questions on any topic including:
- Technology
- Programming
- Electronics
- Science
- Mathematics
- Education
- Career Guidance
- Business
- History 
- Geography
- General Knowledge
- Daily Life Questions
- AI and Machine Learning
- Robotics
- Embedded Systems

Provide accurate, helpful and easy-to-understand answers.
"""
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

            "reply":"AI service unavailable.",

            "title":"Error"

        })
    data = response.json()

    # SUCCESS RESPONSE

    if "choices" in data:

        ai_reply = (
            data["choices"][0]
            ["message"]["content"]
        )

        # AI TITLE GENERATION

        title_prompt = f"""
Generate a short professional title
for this chat.

User message:
{user_message}

Rules:
- Maximum 6 words
- No quotes
- No emojis
- Professional
- Clear and readable
"""

        title_response = requests.post(

            "https://api.groq.com/openai/v1/chat/completions",

            headers=headers,

            json={

                "model": selected_model,

                "messages": [

                    {
                        "role": "system",

                        "content":
                        "Generate short professional chat titles."
                    },

                    {
                        "role": "user",

                        "content": title_prompt
                    }
                ]
            },

            timeout=60
        )

        if title_response.status_code == 200:

            title_data = title_response.json()

        else:
            title_data = {}
            chat_title = "New Chat"


        # TITLE SUCCESS

        if "choices" in title_data:

            chat_title = (

                title_data["choices"][0]
                ["message"]["content"]

                .strip()
            )

        else:

            chat_title = "New Chat"

    # API ERROR

    else:

        ai_reply = f"SRG.ai Error: {data}"

        chat_title = "New Chat"

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