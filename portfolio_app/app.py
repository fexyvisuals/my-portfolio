import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from groq import Groq

load_dotenv()

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please enter a message."}), 400

    # Active supported models on Groq
    active_models = [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b"
    ]

    for model_name in active_models:
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are the AI assistant for FEXY VISUALS. Keep answers friendly, "
                            "professional, concise (1-3 sentences max), and mention flyer design rates "
                            "and direct booking/WhatsApp (+234 708 541 5834) when relevant."
                        )
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                temperature=0.7,
                max_tokens=150
            )
            return jsonify({"response": completion.choices[0].message.content})
        except Exception as e:
            print(f"Model {model_name} error: {e}")
            continue

    # Fallback response if API calls fail
    return jsonify({
        "response": "Thanks for reaching out! You can check our service rates or connect directly with us on WhatsApp (+234 708 541 5834)."
    })

if __name__ == '__main__':
    app.run(debug=True)