from flask import Flask, render_template, request, redirect, url_for
import os
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join('static/data/',file.filename))
        return redirect('/')


if __name__ == '__main__':
    app.run()
