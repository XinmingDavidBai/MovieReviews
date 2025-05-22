from flask import Flask, render_template, request, redirect, url_for
from .db import cur, conn
from .queries import get_all_movies


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html", data = get_all_movies())
