from flask import Flask, render_template
from flask import request, redirect
from flask import flash
from source import sendmessage
import os
SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route('/')
def hello_world():
    return render_template('sendmailer.html')
@app.route('/signup', methods = ['POST'])
def signup():
    email = request.form['message1']
    subject1 = request.form['subject1']
    sendmessage([['Sandeep', 'sunny.bajamahal@gmail.com']], email, subject1)
    flash('Emails successfully sent!')

    return redirect('/')

if __name__ == '__main__':
    app.run()

