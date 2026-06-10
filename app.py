from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os
import requests
from mood_detector import detect_mood_from_image, detect_mood_from_audio

from virtual_tryon import virtual_tryon

WARDROBE_DATA = []

# Import the outfit matching function
from outfit_matcher import analyze_clothing


app = Flask(__name__, static_folder='static')

app.secret_key = "supersecretkey"

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "home"

app.register_blueprint(virtual_tryon)


# Dummy user storage (replace with a database later)
users = {}

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    for email, data in users.items():
        if data["username"] == user_id:
            return User(user_id, data["username"], email)
    return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if email in users:
        flash("Email already exists. Try logging in!", "error")
        return redirect(url_for("home"))

    users[email] = {"username": username, "password": password}
    flash("Account successfully created!", "success")
    return redirect(url_for("home"))

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    if email in users and users[email]["password"] == password:
        user = User(users[email]["username"], users[email]["username"], email)
        login_user(user)
        return redirect(url_for("dashboard"))
    else:
        flash("Invalid credentials. Try again!", "error")
        return redirect(url_for("home"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username)

@app.route("/recommend")
@login_required
def recommend_page():
    return render_template("outfit_recommend.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", "info")
    return redirect(url_for("home"))

# ===============================
# 📌 Outfit Matching Route
# ===============================
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/match", methods=["GET", "POST"])
@login_required
def match():
    if request.method == "POST":
        image = request.files.get("image")
        if image:
            filename = secure_filename(image.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(path)

            result = analyze_clothing(path)
            return render_template("match.html", result=result)

    return render_template("match.html", result=None)

# ===============================
# 🌦️📅 Outfit Recommend Route (Phase 2)
# ===============================
@app.route("/recommend-outfit", methods=["POST"])
def recommend_outfit():
    data = request.get_json()
    city = data["city"]
    event = data["event"]

    # Replace this with your actual OpenWeatherMap API key
    api_key = "b83017acca2e0075a5e1722e8a1e30c3"
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        weather_data = requests.get(weather_url).json()
        temp = weather_data["main"]["temp"]
        condition = weather_data["weather"][0]["main"].lower()

        recommendation = f"For a {event} in {city} where it's {temp}°C and {condition}, you can wear "

        if event == "party":
            recommendation += "a sequin top with jeans or a casual dress with a jacket."
        elif event == "gym":
            recommendation += "light activewear – dry-fit top and shorts or leggings."
        elif event == "formal":
            recommendation += "a tailored suit or a formal blouse with trousers/skirt."
        elif event == "casual":
            recommendation += "a comfy t-shirt and jeans or a floral kurti with leggings."
        elif event == "traditional":
            recommendation += "a kurta-pajama, saree, or salwar kameez."
        elif event == "date":
            recommendation += "a chic dress or a nice shirt with chinos."

        if condition in ["rain", "drizzle"]:
            recommendation += " Don't forget a raincoat or umbrella!"
        elif condition in ["snow"]:
            recommendation += " Wear warm boots and a thick coat."

        return jsonify({"recommendation": recommendation})
    except Exception as e:
        return jsonify({"error": "Weather data could not be fetched. Try a valid city."}), 400
    

    

UPLOAD_MOOD_FOLDER = os.path.join("static", "uploads", "mood")
os.makedirs(UPLOAD_MOOD_FOLDER, exist_ok=True)

@app.route("/mood", methods=["GET", "POST"])
@login_required
def mood_page():
    return render_template("mood.html")

@app.route("/detect-mood-image", methods=["POST"])
@login_required
def detect_mood_image():
    image = request.files.get("image")
    if image:
        filename = secure_filename(image.filename)
        path = os.path.join(UPLOAD_MOOD_FOLDER, filename)
        image.save(path)

        mood = detect_mood_from_image(path)
        recommendation = mood_to_outfit(mood)

        return jsonify({"mood": mood, "recommendation": recommendation})

    return jsonify({"error": "No image uploaded"}), 400

@app.route("/detect-mood-audio", methods=["POST"])
@login_required
def detect_mood_audio():
    audio = request.files.get("audio")
    if audio:
        filename = secure_filename(audio.filename)
        path = os.path.join(UPLOAD_MOOD_FOLDER, filename)
        audio.save(path)

        mood = detect_mood_from_audio(path)
        recommendation = mood_to_outfit(mood)

        return jsonify({"mood": mood, "recommendation": recommendation})

    return jsonify({"error": "No audio uploaded"}), 400

@app.route("/delete_outfit/<int:index>")
@login_required
def delete_outfit(index):

    if index < len(WARDROBE_DATA):

        path = WARDROBE_DATA[index]["path"]

        try:
            os.remove(path[1:])
        except:
            pass

        WARDROBE_DATA.pop(index)

    return redirect("/wardrobe")

@app.route("/favorite/<int:index>")
@login_required
def toggle_favorite(index):

    if index < len(WARDROBE_DATA):
        WARDROBE_DATA[index]["favorite"] = \
        not WARDROBE_DATA[index]["favorite"]

    return redirect("/wardrobe")

@app.route("/wardrobe", methods=["GET", "POST"])
@login_required
def wardrobe():

    if request.method == "POST":

        cloth = request.files.get("cloth")
        category = request.form.get("category")

        if cloth:

            filename = secure_filename(cloth.filename)

            folder = os.path.join(
                "static",
                "wardrobe",
                category
            )

            os.makedirs(folder, exist_ok=True)

            save_path = os.path.join(
                folder,
                filename
            )

            cloth.save(save_path)

            WARDROBE_DATA.append({
                "category": category,
                "path": "/" + save_path.replace("\\", "/"),
                "favorite": False
            })

        return redirect("/wardrobe")

    search = request.args.get("search", "")
    category_filter = request.args.get("category", "")

    filtered = WARDROBE_DATA

    if search:
        filtered = [
            item for item in filtered
            if search.lower() in item["category"].lower()
        ]

    if category_filter:
        filtered = [
            item for item in filtered
            if item["category"] == category_filter
        ]

    stats = {
        "total": len(WARDROBE_DATA),
        "tops": len([x for x in WARDROBE_DATA if x["category"] == "tops"]),
        "bottoms": len([x for x in WARDROBE_DATA if x["category"] == "bottoms"]),
        "dresses": len([x for x in WARDROBE_DATA if x["category"] == "dresses"]),
        "shoes": len([x for x in WARDROBE_DATA if x["category"] == "shoes"]),
        "accessories": len([x for x in WARDROBE_DATA if x["category"] == "accessories"]),
        "favorites": len([x for x in WARDROBE_DATA if x["favorite"]])
    }

    return render_template(
        "wardrobe.html",
        clothes=filtered,
        stats=stats
    )

@app.route("/favorite/<int:index>")
@login_required
def favorite(index):

    if index < len(WARDROBE_DATA):
        WARDROBE_DATA[index]["favorite"] = \
        not WARDROBE_DATA[index]["favorite"]

    return redirect("/wardrobe")

# 🎯 Map mood to outfit suggestion
def mood_to_outfit(mood):
    if mood == "happy":
        return "Wear bright colorful clothes like yellow tops, floral dresses, or cheerful shirts!"
    elif mood == "neutral":
        return "Keep it casual and comfy — jeans, basic tees, hoodies!"
    elif mood == "sad":
        return "Wear cozy soft clothes — oversized sweaters, warm pajamas, soft tracksuits!"
    else:
        return "Couldn't detect mood. Wear what makes you comfortable!"
   



if __name__ == "__main__":
    app.run(debug=True)
