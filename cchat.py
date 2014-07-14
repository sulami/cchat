#!/usr/bin/env python

from flask import Flask, request, render_template, redirect, url_for
from os import urandom
from random import randint
from crypt import crypt

app = Flask(__name__)

app.secret_key = 'ABC123'
salt = 'abcABC123'

sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method != 'POST' or not request.form['password']:
        return redirect(url_for('index'))
    rand = randint(10000, 99999)
    sessions[rand] = crypt(request.form['password'], salt)
    return render_template('chat.html', id=rand)

@app.route('/<int:id>', methods=['GET', 'POST'])
def connect(id):
    if request.method == 'GET':
        return render_template('passwd.html', id=id)
    if id not in sessions:
        return redirect(url_for('index'))
    if crypt(request.form['password'], salt) != sessions[id]:
        return redirect(url_for('index'))
    return "success"

if __name__ == '__main__':
    app.run(debug=True)

