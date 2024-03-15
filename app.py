
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import json
import os

app = Flask(__name__)

@app.route('/clear_data', methods=['POST'])
def clear_data():
    # Clear the data.json file
    with open('data.json', 'w') as f:
        f.truncate(0)
    return redirect(url_for('display'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return redirect(request.url)
            if file:
                df = pd.read_excel(file)
                data = df.to_dict(orient='records')
                with open('data.json', 'a') as f:
                    for entry in data:
                        json.dump(entry, f)
                        f.write('\n')
                return redirect(url_for('display'))  # Redirect to the display page after uploading
        else:
            data = {
                'name': request.form['name'],
                'address': request.form['address'],
                'phone': request.form['phone'],
                'email': request.form['email']
            }
            with open('data.json', 'a') as f:
                json.dump(data, f)
                f.write('\n')
            return render_template('submitted.html', data=data)  # Render submitted.html and pass data
    return render_template('index.html')

@app.route('/display')
def display():
    all_data = []
    with open('data.json', 'r') as f:
        for line in f:
            all_data.append(json.loads(line))
    return render_template('display.html', all_data=all_data)

if __name__ == '__main__':
    app.run(debug=True)
