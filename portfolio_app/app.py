import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from groq import Groq

load_dotenv()

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

# Accepts BOTH /chat and /api/chat so frontends targeting either path will work
@app.route('/chat', methods=['POST'])
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please enter a message."}), 400

    try:
        completion = client.chat.completions.create(
            # Updated to a standard valid Groq model string
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the AI assistant for FEXY VISUALS. Keep answers friendly, "
                        "professional, concise (1-3 sentences max), and mention flyer design rates "
                        "and direct booking/WhatsApp when relevant."
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
        
        reply = completion.choices[0].message.content
        return jsonify({"response": reply})

    except Exception as e:
        print(f"Backend Groq Error: {str(e)}")
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)