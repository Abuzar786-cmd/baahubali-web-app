import json
import os
from flask import Flask, render_template_string, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration for local file uploads
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload folder exists on your computer
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DATA_FILE = "mahishmati_data.json"


def load_data():
    """Load data from local JSON storage."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
                if "warriors" not in data:
                    data["warriors"] = []
                if "songs" not in data:
                    data["songs"] = []
                return data
            except json.JSONDecodeError:
                pass
    return {"warriors": [], "songs": []}


def save_data(data):
    """Save data state to local JSON storage."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Dynamic Full-Stack UI with Local File Uploads
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Baahubali - War Room & Audio Registry</title>
    <style>
        body { 
            margin: 0; padding: 20px;
            background: linear-gradient(135deg, #1a0a00, #3d1400, #0a0500);
            font-family: 'Georgia', serif;
            color: #f1c40f;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
        }
        .container {
            background: rgba(0, 0, 0, 0.88);
            border: 2px solid #d4af37;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 0 25px rgba(212, 175, 55, 0.5);
            width: 520px;
            text-align: center;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        h1 { color: #f39c12; margin-bottom: 5px; font-size: 2.2rem; }
        h2 { color: #d4af37; font-size: 1.3rem; border-bottom: 1px solid #444; padding-bottom: 5px; margin-top: 25px; text-align: left; }
        label { display: block; margin-top: 10px; color: #ecf0f1; font-weight: bold; text-align: left; font-size: 0.9rem; }
        input, select {
            width: 95%; padding: 8px; margin-top: 4px;
            border-radius: 5px; border: 1px solid #d4af37;
            background: #222; color: #fff; font-size: 0.95rem;
        }
        input[type="file"] {
            border: 1px dashed #d4af37;
            background: #111;
            cursor: pointer;
        }
        button {
            margin-top: 15px; background: #d4af37; color: #111;
            border: none; padding: 10px 20px; font-size: 0.95rem;
            font-weight: bold; border-radius: 5px; cursor: pointer;
            width: 100%;
        }
        button:hover { background: #f1c40f; }
        .section-box {
            margin-top: 15px; text-align: left; background: rgba(255, 255, 255, 0.04);
            padding: 12px; border-radius: 8px; border: 1px solid #444;
            max-height: 280px; overflow-y: auto;
        }
        .item-card {
            background: rgba(0,0,0,0.4);
            padding: 10px;
            border-radius: 6px;
            border: 1px solid rgba(212, 175, 55, 0.2);
            margin-bottom: 10px;
        }
        .item-header {
            display: flex; justify-content: space-between; align-items: center;
            color: #e0e0e0; font-size: 0.9rem; margin-bottom: 6px;
        }
        audio {
            width: 100%;
            height: 32px;
            margin-top: 5px;
        }
        .delete-btn {
            background: #c0392b; color: white; border: none;
            padding: 4px 8px; font-size: 0.75rem; border-radius: 4px;
            cursor: pointer; width: auto; margin-top: 0;
        }
        .delete-btn:hover { background: #e74c3c; }
    </style>
</head>
<body>

    <div class="container">
        <h1>MAHISHMATI WAR ROOM</h1>
        <p style="color: #bdc3c7; font-size: 0.95rem;">Manage Army & Local Audio Files</p>
        
        <!-- Warrior Enlistment Form -->
        <h2>⚔️ Enlist Warrior</h2>
        <form action="/" method="POST">
            <input type="hidden" name="form_type" value="add_warrior">
            <label for="warrior_name">Warrior Name:</label>
            <input type="text" id="warrior_name" name="warrior_name" placeholder="e.g. Sivagami" required>
            
            <label for="weapon">Choose Weapon:</label>
            <select id="weapon" name="weapon">
                <option value="Royal Sword ⚔️">Royal Sword ⚔️</option>
                <option value="Heavy Mace 🔨">Heavy Mace 🔨</option>
                <option value="Bow & Fire Arrows 🏹">Bow & Fire Arrows 🏹</option>
            </select>
            
            <button type="submit">Enlist Warrior</button>
        </form>

        <div class="section-box">
            <strong style="color: #f39c12;">Army Roster ({{ data.warriors|length }})</strong>
            {% if data.warriors %}
                {% for w in data.warriors %}
                    <div class="item-card" style="display:flex; justify-content:space-between; align-items:center;">
                        <span><strong>{{ w.name }}</strong> <span style="color:#aaa;">({{ w.weapon }})</span></span>
                        <form action="/" method="POST" style="margin:0;">
                            <input type="hidden" name="form_type" value="delete_warrior">
                            <input type="hidden" name="index" value="{{ loop.index0 }}">
                            <button type="submit" class="delete-btn">Remove</button>
                        </form>
                    </div>
                {% endfor %}
            {% else %}
                <p style="color: #777; font-size: 0.85rem; margin: 8px 0;">No warriors registered.</p>
            {% endif %}
        </div>

        <!-- Music Upload Form (Notice enctype="multipart/form-data") -->
        <h2>🎵 Upload MP3 From Computer</h2>
        <form action="/" method="POST" enctype="multipart/form-data">
            <input type="hidden" name="form_type" value="add_song">
            <label for="song_title">Song / Theme Title:</label>
            <input type="text" id="song_title" name="song_title" placeholder="e.g. Dheevara Theme" required>
            
            <label for="audio_file">Select Audio File (.mp3):</label>
            <input type="file" id="audio_file" name="audio_file" accept=".mp3,audio/*" required>
            
            <button type="submit">Upload & Play</button>
        </form>

        <div class="section-box">
            <strong style="color: #f39c12;">Local Anthems Player ({{ data.songs|length }})</strong>
            {% if data.songs %}
                {% for s in data.songs %}
                    <div class="item-card">
                        <div class="item-header">
                            <span>🎶 <strong>{{ s.title }}</strong></span>
                            <form action="/" method="POST" style="margin:0;">
                                <input type="hidden" name="form_type" value="delete_song">
                                <input type="hidden" name="index" value="{{ loop.index0 }}">
                                <button type="submit" class="delete-btn">Remove</button>
                            </form>
                        </div>
                        <!-- Native HTML5 Audio Player linked to local static file -->
                        <audio controls>
                            <source src="{{ s.url }}" type="audio/mpeg">
                            Your browser does not support the audio element.
                        </audio>
                    </div>
                {% endfor %}
            {% else %}
                <p style="color: #777; font-size: 0.85rem; margin: 8px 0;">No local anthems uploaded yet.</p>
            {% endif %}
        </div>
    </div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    data = load_data()

    if request.method == "POST":
        form_type = request.form.get("form_type")

        # 1. Add Warrior
        if form_type == "add_warrior":
            name = request.form.get("warrior_name")
            weapon = request.form.get("weapon")
            if name and weapon:
                data["warriors"].append({"name": name, "weapon": weapon})
                save_data(data)

        # 2. Delete Warrior
        elif form_type == "delete_warrior":
            try:
                idx = int(request.form.get("index"))
                if 0 <= idx < len(data["warriors"]):
                    data["warriors"].pop(idx)
                    save_data(data)
            except (ValueError, TypeError):
                pass

        # 3. Handle File Upload for Songs
        elif form_type == "add_song":
            title = request.form.get("song_title")
            uploaded_file = request.files.get("audio_file")

            if title and uploaded_file and uploaded_file.filename != "":
                # Secure the filename to prevent malicious paths
                filename = secure_filename(uploaded_file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                
                # Save the file into your project's static folder
                uploaded_file.save(file_path)

                # Store the relative web URL so Flask can serve it
                web_url = f"/static/uploads/{filename}"
                data["songs"].append({"title": title, "url": web_url})
                save_data(data)

        # 4. Delete Song
        elif form_type == "delete_song":
            try:
                idx = int(request.form.get("index"))
                if 0 <= idx < len(data["songs"]):
                    data["songs"].pop(idx)
                    save_data(data)
            except (ValueError, TypeError):
                pass

    return render_template_string(HTML_PAGE, data=data)


if __name__ == "__main__":
    app.run(debug=True)
    from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
