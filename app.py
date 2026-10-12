from flask import Flask, render_template_string, request

app = Flask(__name__)

# Complete Full-Stack Interactive App
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Baahubali - Warrior Registration</title>
    <style>
        body { 
            margin: 0; padding: 0;
            background: linear-gradient(135deg, #1a0a00, #3d1400, #0a0500);
            font-family: 'Georgia', serif;
            color: #f1c40f;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
        }
        .card {
            background: rgba(0, 0, 0, 0.85);
            border: 2px solid #d4af37;
            padding: 35px;
            border-radius: 12px;
            box-shadow: 0 0 25px rgba(212, 175, 55, 0.5);
            width: 380px;
        }
        h1 { color: #f39c12; margin-bottom: 5px; font-size: 2.2rem; }
        label { display: block; margin-top: 15px; color: #ecf0f1; font-weight: bold; }
        input, select {
            width: 90%; padding: 10px; margin-top: 5px;
            border-radius: 5px; border: 1px solid #d4af37;
            background: #222; color: #fff; font-size: 1rem;
        }
        button {
            margin-top: 25px; background: #d4af37; color: #111;
            border: none; padding: 12px 25px; font-size: 1rem;
            font-weight: bold; border-radius: 5px; cursor: pointer;
            width: 95%;
        }
        button:hover { background: #f1c40f; }
        .result-box {
            margin-top: 20px; padding: 15px;
            border: 1px dashed #27ae60; background: rgba(39, 174, 96, 0.1);
            border-radius: 8px; color: #2ecc71;
        }
    </style>
</head>
<body>

    <div class="card">
        <h1>MAHISHMATI</h1>
        <p style="color: #bdc3c7;">Enter your details to join the army</p>
        
        <form action="/" method="POST">
            <label for="warrior_name">Warrior Name:</label>
            <input type="text" id="warrior_name" name="warrior_name" placeholder="e.g. Kattappa" required>
            
            <label for="weapon">Choose Your Weapon:</label>
            <select id="weapon" name="weapon">
                <option value="Royal Sword">⚔️ Royal Sword</option>
                <option value="Mace (Gada)">🔨 Heavy Mace</option>
                <option value="Bow & Fire Arrows">🏹 Bow & Fire Arrows</option>
            </select>
            
            <button type="submit">Enlist for Battle</button>
        </form>

        {% if warrior_name %}
        <div class="result-box">
            <h3>⚔️ Warrior Enlisted!</h3>
            <p><strong>Name:</strong> {{ warrior_name }}</p>
            <p><strong>Weapon:</strong> {{ weapon }}</p>
            <p><i>"Jai Mahishmati! You are ready for war."</i></p>
        </div>
        {% endif %}
    </div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    warrior_name = None
    weapon = None

    # If the user submitted the form (POST request)
    if request.method == "POST":
        warrior_name = request.form.get("warrior_name")
        weapon = request.form.get("weapon")

    return render_template_string(
        HTML_PAGE, warrior_name=warrior_name, weapon=weapon
    )


if __name__ == "__main__":
    app.run(debug=True)