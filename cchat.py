#!/usr/bin/env python

from flask import Flask, request, render_template, redirect, url_for
from os import urandom
from random import randint
from crypt import crypt
from Crypto.Cipher import AES

app = Flask(__name__)

app.secret_key = 'ABC123'
salt = 'abcABC123'
cbc = 'this is 16 bytes'

sessions = {}
content = {}

@app.route('/')
def index():
    return render_template('passwd.html', id='new')

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method != 'POST' or not request.form['password']:
        return redirect(url_for('index'))
    rand = randint(10000, 99999)
    sessions[rand] = crypt(request.form['password'], salt)
    return render_template('message.html', id=rand)

@app.route('/new/<int:id>', methods=['GET', 'POST'])
def write(id):
    if request.method == 'GET':
        return redirect(url_for('index'))
    if id not in sessions:
        return redirect(url_for('index'))
    aes = AES.new(cbc, AES.MODE_CBC, cbc)
    content[id] = aes.encrypt(request.form['message'])
    return render_template('read.html', id=id, message=request.form['message'])

@app.route('/<int:id>', methods=['GET', 'POST'])
def read(id):
    if request.method == 'GET':
        return render_template('passwd.html', id=id)
    if id not in sessions:
        return redirect(url_for('index'))
    if crypt(request.form['password'], salt) != sessions[id]:
        return redirect(url_for('index'))
    aes = AES.new(cbc, AES.MODE_CBC, cbc)
    message = aes.decrypt(content[id])
    return render_template('read.html', id=id, message=message)

if __name__ == '__main__':
    app.run(debug=True)

