from flask import Flask, render_template, request, redirect, url_for, session
import os, pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns
import hdf5storage as hd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.ensemble import IsolationForest

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
        return redirect('/upload')

@app.route('/choose')
def choose():
    file = request.args.get('data')
    session['data'] = file
    return redirect('display')

@app.route('/display')
def display():
    if session['data'].split('.')[-1] == 'csv':
        df = pd.read_csv(os.path.join('static/data/', session['data']))
    elif session['data'].split('.')[-1] == 'mat':
        mat = hd.loadmat(os.path.join('static/data/', session['data']))
        X = pd.DataFrame(mat['X'])
        Y = pd.DataFrame(mat['y'])
        df = pd.concat([X,Y])    
    shape = df.shape
    desc = df.describe().values
    descCol = ['count','mean','std','min','25%','50%','75%','max']
    for idx in range(len(desc)):
        row = list(desc[idx])
        # np.insert(row,0,descCol[idx])
        row.insert(0,descCol[idx])
    print(desc[0])
    tipe = df.dtypes
    
    return render_template('display.html', data=df.values, column=df.columns, shape=shape, descr=desc, tipe=tipe, desccol=descCol)

@app.route('/preprocessing')
def preprocessing():
     pass

@app.route('/forest',  methods=['GET','POST'])
def forest():
    # print(session['data'])
    session['data'] = 'diabetes_new.csv'
    data = pd.read_csv(os.path.join('static/data/', session['data']))
    if request.method == 'GET':
        return render_template('forest.html', column=data.columns)
    else:
        kelas = request.form['kelas']
        normal = request.form['normal']
        abnormal = request.form['abnormal']
        cont = float(request.form['cont'])/100
        n_tree = int(request.form['tree'])
        samples = int(request.form['sample'])
        # Normal Abnormal
        dt_normal=data.loc[data[kelas]==int(normal)]
        dt_abnormal=data.loc[data[kelas]==int(abnormal)]
        # Pisah data
        normal_train, normal_test = train_test_split(dt_normal, test_size=0.7,random_state=42)
        abnormal_train, abnormal_test = train_test_split(dt_abnormal, test_size=0.7,random_state=42)
        train = pd.concat([normal_train, abnormal_train])
        test = pd.concat([normal_test, abnormal_test])
        # Model
        model = IsolationForest(n_estimators=n_tree,contamination=cont, max_samples=samples)
        pred=model.fit_predict(data.drop([kelas],axis=1))
        # Confussion Matrix
        cm2 = confusion_matrix(data[kelas], pred)
        df_cm2 = pd.DataFrame(cm2,['Abnormal','Normal'],['Prediksi Abnormal','Prediksi Normal'])
        plt.figure(figsize = (6,4))
        sns.set(font_scale=1.2)
        sns.heatmap(df_cm2, annot=True, annot_kws={'size':16},fmt='g')
        plt.savefig(os.path.join('static/img/', 'nama.png'))
        
        return render_template('forest.html', cont=cont, tree=n_tree, sample=samples)

if __name__ == '__main__':
    app.run()
