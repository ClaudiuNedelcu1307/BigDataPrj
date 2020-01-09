import os
import sys
############################ COMENZI ACCEPTATE ##############################
from selectProcess import selectQ
from insertProcess import insertQ
from deleteProcess import deleteQ
from dropProcess import dropQ
from createProcess import createQ
from showProcess import showQ
from useProcess import useQ
#############################################################################
import time
import re
from werkzeug.utils import secure_filename
import sqlite3
############################### FLASK CONFIG ################################
from flask import Flask, render_template, request, json, redirect, url_for, flash

template_dir = os.path.abspath('.')
app = Flask(__name__, template_folder=template_dir, root_path=".")
app.static_folder = 'static'
UPLOAD_FOLDER = './uploadFiles'
ALLOWED_EXTENSIONS = {'txt', 'jpg', 'sql'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 160 * 1024 * 1024

validCMDS = ['select', 'delete', 'drop', 'insert', 'update', 'show', 'create', 'use']

@app.route("/")
def main():
    return render_template('index.html')
##############################################################################

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadFile', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return "Success"
        else:
            #flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return 'Bad file'

@app.route('/uploadCmd',methods=['POST'])
def uploadCmd():
    _name = request.form.get('inputName')
    _text = request.form.get('text')
    start_time = time.time()
    noSQL = makeCmd(_name, _text)
    duration = time.time() - start_time
    return {"NoSQL":noSQL, 'duration': duration}

def makeCmd(_name, _text):
    rezList = []
    _text = re.sub('--.*?\n', '', _text)
    cmds = re.split("; *\n+", _text)
    i = 1
    for cmd in cmds:
        cmd = cmd.replace(';', '')
        cmd = cmd.replace('\n', ' ')
        cmd = cmd.replace('(', ' ( ')
        cmd = cmd.replace(')', ' ) ')
        cmd = cmd.replace(',', ', ')
        cmd.lower()
        cmd = re.sub(' +', ' ', cmd.strip())
        textList = cmd.split()
        # validate the received values validarea comenzi
        if textList:
            if textList[0].lower() in validCMDS:
                tempDict = {}
                tempDict['val'] = textList
                # apelare metoda pentru fiecare nod
                rezEval = eval(str(textList[0].lower()) + 'Q' + '(' + str(tempDict) + ')')
                rezList.append(rezEval)
            else: 
                rezList.append('The ' + str(i) +' query can not be converted !')
            i = i + 1
    
    return '\n'.join(rezList)

@app.route('/resolveFile',methods=['GET'])
def resolveFile():
    start_time = time.time()
    _name = request.args.get('fileName')

    _name = os.path.join(app.config['UPLOAD_FOLDER'], _name)
    f = open(_name, "r")
    sql = f.read()
    noSQL = makeCmd('select', sql)

    duration = time.time() - start_time
    print("--- %s seconds ---" % (duration))
    return {"NoSQL":noSQL, 'duration': duration}



if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True, use_reloader=False)