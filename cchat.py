#!/usr/bin/env python

from flask import Flask, request, render_template, redirect, url_for, sessions
from os import urandom
from random import randint

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method != 'POST' or not request.form['password']:
        return redirect(url_for('index'))
    rand = randint(10000, 99999)
    return render_template('chat.html', id=rand)

@app.route('/<int:id>')
def connect(id):
    return str(id)

if __name__ == '__main__':
    app.run(debug=True)

