import os

import openai
from flask import Flask, redirect, render_template, request, url_for

from core.vector_db import Storage
from core.user_query import get_answer

app = Flask(__name__)
storage = Storage()
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        user_question = request.form["question"]
        bot_answer = get_answer(storage, user_question)
        return redirect(url_for("index", result=bot_answer))

    result = request.args.get("result")
    return render_template("index.html", result=result)
