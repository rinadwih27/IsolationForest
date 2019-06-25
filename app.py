from flask import Flask, render_template, request, redirect, url_for, session
import os, pandas as pd

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/',  methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        nama = request.form['nama']
        return nama

@app.route('/login')
def login():
    session['username'] = 'rakumairu'
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        files = []
        for r, d, f in os.walk('static/data'):
            for file in f:
                if '.csv' in file or '.mat' in file:
                    files.append(file)
        return render_template('upload.html', files=files)
    elif request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join('static/data/',file.filename))
        return redirect('/')

@app.route('/choose')
def choose():
    file = request.args.get('data')
    session['data'] = file
    return redirect('display')

@app.route('/display')
def display():
    df = pd.read_csv(os.path.join('static/data/', session['data']))
    shape = df.shape
    return render_template('display.html', data=df.values, column=df.columns, shape=shape)

@app.route('/preprocessing')
def preprocessing():
    pass

@app.route('/forest',  methods=['GET','POST'])
def forest():
    if request.method == 'GET':
        return render_template('forest.html')
    else:
        nama = request.form['nama']
        nim = request.form['nim']
        return render_template('forest.html', nama=nama, nim=nim)


if __name__ == '__main__':
    app.run()
