from flask import Flask, render_template, request, send_file, url_for,make_response,redirect
import os
import sqlite3

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DATABASE = 'files.db'

def create_connection():
    conn = sqlite3.connect(DATABASE)
    return conn

def create_upload_directory():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM files")
    files = cursor.fetchall()
    conn.close()
    return render_template('index.html', encrypted_files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    create_upload_directory()  # Ensure that the upload directory exists
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename.strip()  # Remove leading and trailing spaces from filename
            encrypted_filename = 'encrypted_' + filename
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO files (filename, encrypted_filename) VALUES (?, ?)", (filename, encrypted_filename))
            conn.commit()
            conn.close()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], encrypted_filename))
    return make_response('',204)


@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
