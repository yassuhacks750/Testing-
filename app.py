from flask import Flask, request, render_template, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    folders = {}
    for folder in os.listdir(UPLOAD_FOLDER):
        folder_path = os.path.join(UPLOAD_FOLDER, folder)
        if os.path.isdir(folder_path):
            images = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
            folders[folder] = images
    return render_template('index.html', folders=folders)

@app.route('/upload', methods=['POST'])
def upload():
    folder = request.form.get('folder')
    file = request.files['image']
    save_path = os.path.join(UPLOAD_FOLDER, folder)
    os.makedirs(save_path, exist_ok=True)
    file.save(os.path.join(save_path, file.filename))
    return 'Uploaded', 200

@app.route('/uploads/<folder>/<filename>')
def uploaded_file(folder, filename):
    return send_from_directory(os.path.join(UPLOAD_FOLDER, folder), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
