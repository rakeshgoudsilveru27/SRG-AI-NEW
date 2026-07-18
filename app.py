from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import requests
import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY not found")
print(
    "GROQ FOUND:",
    bool(GROQ_API_KEY)
)


DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY")

if not DEEPGRAM_API_KEY:
    print("WARNING: DEEPGRAM_API_KEY not found")
else:
    print("DEEPGRAM FOUND")


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

OPENWEATHER_API_KEY = os.environ.get(
    "OPENWEATHER_API_KEY"
)

GEMINI_KEYS = [
    os.getenv("GEMINI_API_KEY"),
    os.getenv("GEMINI_API_KEY1"),
    os.getenv("GEMINI_API_KEY2"),
    os.getenv("GEMINI_API_KEY3"),
]

GEMINI_KEYS = [k for k in GEMINI_KEYS if k]

print("Gemini Keys Loaded:", len(GEMINI_KEYS))

def ask_gemini(prompt):

    last_error = None

    for index, api_key in enumerate(GEMINI_KEYS):

        try:

            print(f"Using Gemini Key {index+1}")

            genai.configure(api_key=api_key)

            model = genai.GenerativeModel(
                "gemini-2.5-flash"
            )

            response = model.generate_content(prompt)

            if hasattr(response, "text"):
                return response.text

            return "No response."

        except Exception as e:

            print(f"Gemini Key {index+1} Failed")

            print(e)

            last_error = e

            # Only continue for quota/rate limit errors.
            error_text = str(e).lower()
            if "429" in error_text or "quota" in error_text or "rate limit" in error_text:
                continue

            # For other errors, stop immediately.
            raise

    raise last_error


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

            def ask_gemini_vision(prompt, img):

                last_error = None

                for index, api_key in enumerate(GEMINI_KEYS):

                    try:

                        print(f"Vision using Key {index+1}")

                        genai.configure(api_key=api_key)

                        model = genai.GenerativeModel(
                            "gemini-2.5-flash"
                        )

                        response = model.generate_content(
                           [prompt, img]
                        )

                        return response.text

                    except Exception as e:

                        print(e)

                        last_error = e

                        error_text = str(e).lower()
                        if "429" in error_text or "quota" in error_text or "rate limit" in error_text:
                            continue

                        raise

                raise last_error

            ai_reply = ask_gemini_vision(user_message, img)

            print("GEMINI RESPONSE RECEIVED")
            print(ai_reply)

            ai_reply = ask_gemini_vision(
                user_message,
                img
            )

            print(ai_reply)

            conversation_history.append(
                f"User: {user_message}"
            )

            conversation_history.append(
                f"Assistant: {ai_reply}"
            )

            conversation_history[:] = conversation_history[-20:]

            return jsonify({

                "reply": ai_reply,

                "title": user_message[:30]

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

You are a highly specialized AI assistant focused on:

1. Embedded Systems
2. Electronics
3. IoT
4. Robotics
5. PCB Design
6. VLSI
7. Programming
8. Artificial Intelligence
9. Engineering Projects

These are your primary specializations and you should provide detailed expert-level answers in these areas.

For all other topics such as:
- General Knowledge
- History
- Geography
- Science
- Mathematics
- Daily Life
- Career Guidance

you should still answer accurately and helpfully.

Rules:
- Prioritize technical and engineering excellence.
- Give step-by-step explanations.
- For coding, provide complete code.
- For electronics, explain components, connections and troubleshooting.
- For VLSI, explain concepts clearly.
- For general questions, answer normally.
- Never invent facts.

Conversation History:
{history}

{prompt_image_text if image else ""}

User:
{user_message}

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
        ai_reply = ask_gemini(prompt)

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

@app.route("/glasses", methods=["GET", "POST"])
def glasses():

    # Browser test
    if request.method == "GET":
        return jsonify({
            "status": "working",
            "message": "SRG Glasses API is running."
        })

    # POST request from ESP32
    data = request.get_json(silent=True) or {}

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "status": "error",
            "reply": "Please enter a message."
        }), 400

    try:

        prompt = f"""
You are SRG.ai.

Reply briefly because the answer will be spoken by AI glasses.

User:
{user_message}
"""

        ai_reply = ask_gemini(prompt)

        return jsonify({
            "status": "success",
            "reply": ai_reply
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "reply": f"AI Error: {str(e)}"
        }), 500

@app.route("/glasses_voice", methods=["GET", "POST"])
def glasses_voice():

    # Browser test
    if request.method == "GET":
        return jsonify({
            "status": "working",
            "message": "SRG Voice API is running."
        })

    # Check audio file
    if "audio" not in request.files:
        return jsonify({
            "status": "error",
            "reply": "No audio file received."
        }), 400

    audio = request.files["audio"]

    if audio.filename == "":
        return jsonify({
            "status": "error",
            "reply": "No audio file selected."
        }), 400

    audio_data = audio.read()

    try:
        # Send audio to Deepgram
        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "audio/wav"
        }

        response = requests.post(
            "https://api.deepgram.com/v1/listen?model=nova-3&smart_format=true",
            headers=headers,
            data=audio_data,
            timeout=60
        )

        if response.status_code != 200:
            return jsonify({
                "status": "error",
                "reply": "Deepgram transcription failed.",
                "details": response.text
            }), 500

        dg = response.json()

        transcript = (
            dg.get("results", {})
              .get("channels", [{}])[0]
              .get("alternatives", [{}])[0]
              .get("transcript", "")
        )

        if not transcript:
            return jsonify({
                "status": "error",
                "reply": "No speech detected."
            }), 400

        print("USER SAID:", transcript)

        # Ask Gemini
        prompt = f"""
You are SRG glasses with SRG.ai integrated 

Reply briefly because the answer will be spoken by AI glasses.

User:
{transcript}
"""

        reply = ask_gemini(prompt)

        return jsonify({
            "status": "success",
            "heard": transcript,
            "reply": reply
        })

    except Exception as e:
        print("VOICE ERROR:", str(e))

        return jsonify({
            "status": "error",
            "reply": str(e)
        }), 500