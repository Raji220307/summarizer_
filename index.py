from flask import Flask, render_template, request
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("Warning: GROQ_API_KEY not set. The app will fail if you try to call the API.")

client = Groq(api_key=api_key)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    error_message = None

    if request.method == "POST":
        paragraph = request.form.get("paragraph", "").strip()

        if paragraph:
            prompt = f"""
            Read the following paragraph carefully and summarize all its content
            in one concise sentence:

            {paragraph}
            """
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=100
                )
                summary = response.choices[0].message.content
            except Exception as e:
                error_message = f"Error calling Groq API: {e}"
        else:
            error_message = "Please enter a paragraph."

    return render_template("index.html", summary=summary, error_message=error_message)

# Needed for Vercel deployment
app = app

# Enable local testing
if __name__ == "__main__":
    app.run(debug=True)
