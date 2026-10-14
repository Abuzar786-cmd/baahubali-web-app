import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = os.path.join('static', 'audio')
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# In-memory storage for warrior track data
warrior_tracks = [
    {
        "warrior": "Amarendra Baahubali",
        "theme": "Mahishmati Royal Anthem",
        "filename": "theme_song.mp3"
    }
]

@app.route('/')
def home():
    return render_template('index.html', tracks=warrior_tracks)

@app.route('/upload', methods=['POST'])
def upload_file():
    warrior = request.form.get('warrior_name', 'Unknown Warrior')
    theme = request.form.get('theme_name', 'Custom Theme')
    
    if 'audio_file' not in request.files:
        return redirect(request.url)
    
    file = request.files['audio_file']
    
    if file.filename == '':
        return redirect(request.url)
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Save track entry
        warrior_tracks.append({
            "warrior": warrior,
            "theme": theme,
            "filename": filename
        })
        
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
