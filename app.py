from flask import Flask, render_template
from flask import request, redirect
from source import sendmessage
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')
@app.route('/signup', methods = ['POST'])
def signup():
    email = request.form['message1']
    sendfile = request.form['fileoname']
    sendmessage([['Sandeep', 'sunny.bajamahal@gmail.com']], email, 'subject')

    return redirect('/')

if __name__ == '__main__':
    app.run()

