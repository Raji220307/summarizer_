from flask import Flask, render_template, request
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    error_message = None
    if request.method == "POST":
        paragraph = request.form.get("paragraph")
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
                error_message = "Error generating summary. Check API key or usage."
        else:
            error_message = "Please enter a paragraph."

    return render_template("index.html", summary=summary, error_message=error_message)

# Required for Vercel serverless
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

app = app  
