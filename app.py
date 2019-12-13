import os
import sys
from selectProcess import selectQ
from insertProcess import insertQ
from deleteProcess import deleteQ
from dropProcess import dropQ
from createProcess import createQ
from showProcess import showQ
import re
from werkzeug.utils import secure_filename
############################### FLASK CONFIG ################################
from flask import Flask, render_template, request, json, redirect, url_for, flash

template_dir = os.path.abspath('.')
app = Flask(__name__, template_folder=template_dir, root_path=".")
app.static_folder = 'static'
UPLOAD_FOLDER = './uploadFiles'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'jpg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

validCMDS = ['select', 'delete', 'drop', 'insert', 'update', 'show', 'create']

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
            return "Mata probeaza, Catalin nu probeaza!"
        else:
            #flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return 'Fisier prost ca tine'

@app.route('/uploadCmd',methods=['POST'])
def uploadCmd():
    _name = request.form.get('inputName')
    _text = request.form.get('text')
    return makeCmd(_name, _text)

def makeCmd(_name, _text):
    rezList = []
    cmds = re.split("; *\n+", _text)
    print(cmds)
    for cmd in cmds:
        cmd = cmd.replace(';', '')
        cmd = cmd.replace('(', ' ( ')
        cmd = cmd.replace(')', ' ) ')
        cmd.lower()
        cmd = re.sub(' +', ' ', cmd.strip())
        textList = cmd.split()
        print(textList)
        # validate the received values
        if textList:
            if textList[0] in validCMDS:
                tempDict = {}
                tempDict['val'] = textList
                rezEval = eval(str(textList[0]) + 'Q' + '(' + str(tempDict) + ')')
                rezList.append(rezEval)
            else: 
                return 'Put a sock on it !'
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    
    return '\n'.join(rezList)

@app.route('/resolveFile',methods=['GET'])
def resolveFile():
    # return {"noSQL":"Two hand pierce", "SQL":"Dead Space Monkey"}
    _name = request.form.get('fileName')
    _name = "test.txt"
    _name = os.path.join(app.config['UPLOAD_FOLDER'], _name)
    f = open(_name, "r")
    sql = f.read()
    noSQL = makeCmd('select', sql)
    return {"noSQL":noSQL, "SQL":sql}



if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True, use_reloader=False)