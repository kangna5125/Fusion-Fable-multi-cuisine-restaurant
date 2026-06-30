import json, os, uuid
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, session, redirect, url_for, request, flash

app = Flask(__name__)
app.secret_key = "fusion_fable_secret_key_2024"

USERS_FILE = "users.json"

# ── Menu data ────────────────────────────────────────────────────────────────
MENU = {
    # ── Starters (shared across cuisines) ────────────────────────────────────
    "veg_starters": {
        "title": "Veg Starters",
        "back": "/starters",
        "css": "static2.css",
        "items": [
            {"name": "Paneer Tikka",         "img": "5.1.jpg",  "price": 220},
            {"name": "Seekh Kabab",           "img": "5.2.jpg",  "price": 180},
            {"name": "Hara Bhara Kabab",      "img": "5.3.jpg",  "price": 180},
            {"name": "Shanghai Spring Roll",  "img": "5.4.jpg",  "price": 190},
            {"name": "American Corn Ball",    "img": "5.5.jpg",  "price": 170},
            {"name": "Crispy American Corn",  "img": "5.6.jpg",  "price": 160},
            {"name": "Crispy Baby Corn",      "img": "5.7.jpg",  "price": 170},
            {"name": "Crispy Mushroom",       "img": "5.8.jpg",  "price": 190},
            {"name": "Crispy Chilly Potato",  "img": "5.9.jpg",  "price": 160},
            {"name": "Crispy Chilly Chana",   "img": "5.10.jpg", "price": 160},
        ]
    },
    "nonveg_starters": {
        "title": "Non-Veg Starters",
        "back": "/starters",
        "css": "static4.css",
        "items": [
            {"name": "Chicken Tikka",       "img": "1.1.jpg",  "price": 280},
            {"name": "Murg Reshmi Kabab",   "img": "1.2.jpg",  "price": 290},
            {"name": "Murg Chilli Kabab",   "img": "1.3.jpg",  "price": 290},
            {"name": "Chicken Seekh Kabab", "img": "1.4.jpg",  "price": 280},
            {"name": "Tandoori Kabab",      "img": "1.5.jpg",  "price": 300},
            {"name": "Murg Tandoor",        "img": "1.6.jpg",  "price": 300},
            {"name": "Fish Ajwani Tikka",   "img": "1.7.jpg",  "price": 320},
            {"name": "Chilli Chicken",      "img": "1.8.jpg",  "price": 270},
            {"name": "Drums of Heaven",     "img": "1.9.jpg",  "price": 280},
            {"name": "Shanghai Chicken",    "img": "1.10.jpg", "price": 290},
        ]
    },

    # ── Indian Main Course ────────────────────────────────────────────────────
    "indian_veg": {
        "title": "Indian Veg Dishes",
        "back": "/cuisine/indian",
        "css": "static5.css",
        "items": [
            {"name": "Kadhai Paneer",        "img": "11.1.jpg",  "price": 260},
            {"name": "Matar Paneer",         "img": "11.2.jpg",  "price": 240},
            {"name": "Paneer Butter Masala", "img": "11.3.jpg",  "price": 260},
            {"name": "Malai Kofta",          "img": "11.4.jpg",  "price": 250},
            {"name": "Navratan Korma",       "img": "11.5.jpg",  "price": 260},
            {"name": "Kadhai Vegetable",     "img": "11.6.jpg",  "price": 220},
            {"name": "Dum Aloo",             "img": "11.7.jpg",  "price": 220},
            {"name": "Palak Paneer",         "img": "11.8.jpg",  "price": 240},
            {"name": "Tawa Pulao",           "img": "11.9.jpg",  "price": 200},
            {"name": "Kashmiri Pulao",       "img": "11.10.jpg", "price": 220},
            {"name": "Butter Naan",          "img": "11.11.jpg", "price": 60},
            {"name": "Stuffed Kulcha",       "img": "11.12.jpg", "price": 80},
        ]
    },
    "indian_nonveg": {
        "title": "Indian Non-Veg Dishes",
        "back": "/cuisine/indian",
        "css": "static6.css",
        "items": [
            {"name": "Chicken Tikka Masala",  "img": "12.1.jpg",  "price": 320},
            {"name": "Chicken Tikka Labadar", "img": "12.2.jpg",  "price": 330},
            {"name": "Chicken Bharta",        "img": "12.3.jpg",  "price": 310},
            {"name": "Kadhai Chicken",        "img": "12.4.jpg",  "price": 320},
            {"name": "Mughlai Chicken",       "img": "12.5.jpg",  "price": 340},
            {"name": "Murg Navratan Korma",   "img": "12.6.jpg",  "price": 350},
            {"name": "Chicken Do Pyaaz",      "img": "12.7.jpg",  "price": 320},
            {"name": "Murg Masallam",         "img": "12.8.jpg",  "price": 360},
            {"name": "Mutton Rogan Josh",     "img": "12.9.jpg",  "price": 380},
            {"name": "Prawn Malai Curry",     "img": "12.10.jpg", "price": 400},
            {"name": "Fish Sarsowala",        "img": "12.11.jpg", "price": 360},
            {"name": "Murg Makhani",          "img": "12.12.jpg", "price": 340},
        ]
    },

    # ── Chinese Main Course ───────────────────────────────────────────────────
    "chinese_veg": {
        "title": "Chinese Veg Dishes",
        "back": "/cuisine/chinese",
        "css": "static7.css",
        "items": [
            {"name": "Schezwan Fried Rice",  "img": "13.1.png",  "price": 220},
            {"name": "Veg Hakka Noodle",     "img": "13.5.png",  "price": 200},
            {"name": "Paneer Manchurian",    "img": "13.7.png",  "price": 240},
            {"name": "Shanghai Fried Rice",  "img": "13.8.png",  "price": 220},
            {"name": "Veg Fried Rice",       "img": "13.9.png",  "price": 200},
            {"name": "Kimchi Rice Veg",      "img": "13.10.png", "price": 210},
            {"name": "Veg Spring Roll",      "img": "13.12.png", "price": 190},
        ]
    },
    "chinese_nonveg": {
        "title": "Chinese Non-Veg Dishes",
        "back": "/cuisine/chinese",
        "css": "static7.css",
        "items": [
            {"name": "Schezwan Chicken",     "img": "13.2.png",  "price": 280},
            {"name": "Chilly Chicken",       "img": "13.3.png",  "price": 270},
            {"name": "Chicken Noodle",       "img": "13.4.png",  "price": 250},
            {"name": "Chicken Manchurian",   "img": "13.6.png",  "price": 280},
            {"name": "Chicken Fried Rice",   "img": "13.11.png", "price": 240},
        ]
    },

    # ── Italian Main Course ───────────────────────────────────────────────────
    "italian_veg": {
        "title": "Italian Veg Dishes",
        "back": "/cuisine/italian",
        "css": "static5.css",
        "items": [
            {"name": "Spaghetti Aglio e Olio",  "img": "15.1.jpg",  "price": 280},
            {"name": "Margherita Pizza",         "img": "15.2.jpg",  "price": 320},
            {"name": "Mushroom Risotto",         "img": "15.3.jpg",  "price": 300},
            {"name": "Veg Lasagna",              "img": "15.4.jpg",  "price": 310},
            {"name": "Penne Arrabbiata",         "img": "15.5.jpg",  "price": 260},
            {"name": "Bruschetta al Pomodoro",   "img": "15.6.jpg",  "price": 180},
            {"name": "Fettuccine Alfredo",       "img": "15.7.jpg",  "price": 290},
            {"name": "Minestrone Soup",          "img": "15.8.jpg",  "price": 220},
            {"name": "Potato Gnocchi",           "img": "15.9.jpg", "price": 270},
            {"name": "Four Cheese Pizza",        "img": "15.10.jpg",  "price": 350},
            {"name": "Garlic Bread",             "img": "15.11.jpg",  "price": 120},
            {"name": "Tiramisu",                 "img": "15.12.jpg",  "price": 180},
        ]
    },
    "italian_nonveg": {
        "title": "Italian Non-Veg Dishes",
        "back": "/cuisine/italian",
        "css": "static6.css",
        "items": [
            {"name": "Chicken Parmesan",         "img": "15.13.png", "price": 380},
            {"name": "Osso Buco",                "img": "15.14.png", "price": 420},
            {"name": "Chicken Carbonara",        "img": "15.15.png",  "price": 360},
            {"name": "Prawn Linguine",           "img": "15.16.png",  "price": 400},
            {"name": "Chicken Pesto Pasta",      "img": "15.17.png",  "price": 350},
            {"name": "Seafood Risotto",          "img": "15.18.png",  "price": 420},
            {"name": "Meat Lover's Pizza",       "img": "15.19.png",  "price": 390},
            {"name": "Chicken Cacciatore",       "img": "15.20.png", "price": 380},
            {"name": "Beef Bolognese",           "img": "15.21.png",  "price": 370},
            {"name": "Grilled Salmon Piccata",   "img": "15.22.png", "price": 440},
            {"name": "Chicken Marsala",          "img": "15.23.png", "price": 360},
            {"name": "Tuna Pasta Bake",          "img": "15.24.png",  "price": 340},
        ]
    },

    # ── Mexican Main Course ───────────────────────────────────────────────────
    "mexican_veg": {
        "title": "Mexican Veg Dishes",
        "back": "/cuisine/mexican",
        "css": "static5.css",
        "items": [
            {"name": "Veg Tacos",               "img": "16.1.png",  "price": 240},
            {"name": "Bean & Cheese Burrito",   "img": "16.2.png",  "price": 260},
            {"name": "Veg Quesadilla",          "img": "16.3.png",  "price": 220},
            {"name": "Guacamole & Nachos",      "img": "16.4.png",  "price": 200},
            {"name": "Veg Enchiladas",          "img": "16.5.png",  "price": 270},
            {"name": "Black Bean Bowl",         "img": "16.6.png",  "price": 230},
            {"name": "Corn Tortilla Soup",      "img": "16.7.png",  "price": 210},
            {"name": "Stuffed Peppers",         "img": "16.8.png",  "price": 250},
            {"name": "Veg Fajitas",             "img": "16.9.png",  "price": 280},
            {"name": "Pico de Gallo Salad",     "img": "16.10.png", "price": 180},
            {"name": "Cheese Nachos",           "img": "16.11.png",  "price": 190},
            {"name": "Spanish Rice Bowl",       "img": "16.12.png", "price": 220},
        ]
    },
    "mexican_nonveg": {
        "title": "Mexican Non-Veg Dishes",
        "back": "/cuisine/mexican",
        "css": "static6.css",
        "items": [
            {"name": "Chicken Tacos",           "img": "16.13.png",  "price": 290},
            {"name": "Chicken Burrito",         "img": "16.14.png",  "price": 310},
            {"name": "Chicken Quesadilla",      "img": "16.15.png",  "price": 270},
            {"name": "Pulled Pork Nachos",      "img": "16.16.png",  "price": 320},
            {"name": "Chicken Enchiladas",      "img": "16.17.png",  "price": 320},
            {"name": "Beef Burrito Bowl",       "img": "16.18.png",  "price": 340},
            {"name": "Chicken Tortilla Soup",   "img": "16.19.png",  "price": 260},
            {"name": "Shrimp Fajitas",          "img": "16.20.png",  "price": 360},
            {"name": "Carnitas Taco Bowl",      "img": "16.21.png", "price": 330},
            {"name": "Fish Tacos Baja Style",   "img": "16.22.png",  "price": 300},
            {"name": "Chicken Tinga Tostadas",  "img": "16.23.png", "price": 280},
            {"name": "Beef Chilli con Carne",   "img": "16.24.png", "price": 310},
        ]
    },

    # ── Desserts ──────────────────────────────────────────────────────────────
    "desserts": {
        "title": "Desserts",
        "back": "/",
        "css": "static8.css",
        "items": [
            {"name": "Softy Pineapple",            "img": "14.5.jpg",  "price": 120},
            {"name": "Softy Crunchy Chocolate",    "img": "14.6.jpg",  "price": 130},
            {"name": "Chocolate Walnut Brownie",   "img": "14.7.jpg",  "price": 150},
            {"name": "Chocolate Doughnut",         "img": "14.4.jpg",  "price": 130},
            {"name": "Marble Cake",                "img": "14.8.jpg",  "price": 160},
            {"name": "Mocha Magic",                "img": "14.3.jpg",  "price": 140},
            {"name": "Black Forest Cake",          "img": "14.9.jpg",  "price": 180},
            {"name": "Mango Shake",                "img": "14.2.jpg",  "price": 120},
            {"name": "Pineapple Shake",            "img": "14.1.jpg",  "price": 120},
        ]
    },
}

# ── Cuisine definitions ────────────────────────────────────────────────────────
CUISINES = {
    "indian": {
        "name": "Indian",
        "emoji": "🇮🇳",
        "tagline": "Rich curries, tandoor classics & aromatic spices",
        "banner": "indian_banner.jpg",
        "veg_key": "indian_veg",
        "nonveg_key": "indian_nonveg",
    },
    "chinese": {
        "name": "Chinese",
        "emoji": "🥢",
        "tagline": "Wok-tossed noodles, fried rice & bold sauces",
        "banner": "chinese_banner.jpg",
        "veg_key": "chinese_veg",
        "nonveg_key": "chinese_nonveg",
    },
    "italian": {
        "name": "Italian",
        "emoji": "🍕",
        "tagline": "Handmade pasta, wood-fired pizza & creamy risottos",
        "banner": "italian_banner.jpg",
        "veg_key": "italian_veg",
        "nonveg_key": "italian_nonveg",
    },
    "mexican": {
        "name": "Mexican",
        "emoji": "🌮",
        "tagline": "Sizzling fajitas, loaded tacos & fiesta flavours",
        "banner": "mexican_banner.jpg",
        "veg_key": "mexican_veg",
        "nonveg_key": "mexican_nonveg",
    },
}

# ── User helpers ──────────────────────────────────────────────────────────────
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE) as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

# ── Cart helpers ──────────────────────────────────────────────────────────────
def get_cart():
    return session.get("cart", {})

def cart_count():
    return sum(item["qty"] for item in get_cart().values())

def cart_total():
    return sum(item["price"] * item["qty"] for item in get_cart().values())

app.jinja_env.globals["cart_count"] = cart_count

# ── Auth routes ───────────────────────────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        users = load_users()
        if username in users and users[username]["password"] == password:
            session["user"] = username
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for("home"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user" in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirm  = request.form.get("confirm", "").strip()
        users = load_users()
        if not username or not password:
            flash("Username and password are required.", "danger")
        elif username in users:
            flash("Username already taken. Try another.", "danger")
        elif password != confirm:
            flash("Passwords do not match.", "danger")
        else:
            users[username] = {"password": password}
            save_users(users)
            session["user"] = username
            flash(f"Account created! Welcome, {username}!", "success")
            return redirect(url_for("home"))
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# ── Menu routes ───────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/starters")
def starters():
    return render_template("starters.html")

# ── NEW: Choose Cuisine ───────────────────────────────────────────────────────
@app.route("/choose-cuisine")
def choose_cuisine():
    return render_template("choose_cuisine.html", cuisines=CUISINES)

@app.route("/cuisine/<cuisine_id>")
def cuisine_detail(cuisine_id):
    cuisine = CUISINES.get(cuisine_id)
    if not cuisine:
        flash("Cuisine not found.", "danger")
        return redirect(url_for("choose_cuisine"))
    return render_template("cuisine_detail.html", cuisine=cuisine, cuisine_id=cuisine_id)

# ── Legacy main-course (redirect to choose-cuisine) ───────────────────────────
@app.route("/main-course")
def maincourse():
    return redirect(url_for("choose_cuisine"))

# ── Legacy direct routes (kept for backward compatibility) ────────────────────
@app.route("/vegstarters")
def vegstarters():
    data = MENU["veg_starters"]
    return render_template("menu_page.html", **data)

@app.route("/non-vegstarters")
def nonvegstarters():
    data = MENU["nonveg_starters"]
    return render_template("menu_page.html", **data)

@app.route("/IndianVegDishes")
def IndianVegDishes():
    data = MENU["indian_veg"]
    return render_template("menu_page.html", **data)

@app.route("/IndianNonVegDishes")
def IndianNonVegDishes():
    data = MENU["indian_nonveg"]
    return render_template("menu_page.html", **data)

@app.route("/ChineseVegDishes")
def ChineseVegDishes():
    data = MENU["chinese_veg"]
    return render_template("menu_page.html", **data)

@app.route("/ChineseNonVegDishes")
def ChineseNonVegDishes():
    data = MENU["chinese_nonveg"]
    return render_template("menu_page.html", **data)

@app.route("/ChineseDishes")
def ChineseDishes():
    return redirect(url_for("cuisine_detail", cuisine_id="chinese"))

# ── NEW: Italian & Mexican routes ─────────────────────────────────────────────
@app.route("/ItalianVegDishes")
def ItalianVegDishes():
    data = MENU["italian_veg"]
    return render_template("menu_page.html", **data)

@app.route("/ItalianNonVegDishes")
def ItalianNonVegDishes():
    data = MENU["italian_nonveg"]
    return render_template("menu_page.html", **data)

@app.route("/MexicanVegDishes")
def MexicanVegDishes():
    data = MENU["mexican_veg"]
    return render_template("menu_page.html", **data)

@app.route("/MexicanNonVegDishes")
def MexicanNonVegDishes():
    data = MENU["mexican_nonveg"]
    return render_template("menu_page.html", **data)

@app.route("/dessert")
def dessert():
    data = MENU["desserts"]
    return render_template("menu_page.html", **data)

# ── Cart routes ───────────────────────────────────────────────────────────────
@app.route("/cart/add", methods=["POST"])
@login_required
def add_to_cart():
    name  = request.form.get("name")
    price = int(request.form.get("price", 0))
    img   = request.form.get("img", "")
    qty   = int(request.form.get("qty", 1))
    cart  = get_cart()
    if name in cart:
        cart[name]["qty"] += qty
    else:
        cart[name] = {"price": price, "qty": qty, "img": img}
    session["cart"] = cart
    flash(f"'{name}' added to cart!", "success")
    return redirect(request.referrer or url_for("home"))

@app.route("/cart/update", methods=["POST"])
@login_required
def update_cart():
    name = request.form.get("name")
    qty  = int(request.form.get("qty", 1))
    cart = get_cart()
    if name in cart:
        if qty <= 0:
            del cart[name]
        else:
            cart[name]["qty"] = qty
    session["cart"] = cart
    return redirect(url_for("view_cart"))

@app.route("/cart/remove", methods=["POST"])
@login_required
def remove_from_cart():
    name = request.form.get("name")
    cart = get_cart()
    cart.pop(name, None)
    session["cart"] = cart
    flash(f"'{name}' removed from cart.", "info")
    return redirect(url_for("view_cart"))

@app.route("/cart")
@login_required
def view_cart():
    cart = get_cart()
    subtotal = cart_total()
    gst      = round(subtotal * 0.05, 2)
    total    = round(subtotal + gst, 2)
    return render_template("cart.html", cart=cart,
                           subtotal=subtotal, gst=gst, total=total)

# ── Order routes ──────────────────────────────────────────────────────────────
@app.route("/order/place", methods=["POST"])
@login_required
def place_order():
    cart = get_cart()
    if not cart:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("view_cart"))

    subtotal   = cart_total()
    gst        = round(subtotal * 0.05, 2)
    total      = round(subtotal + gst, 2)
    order_id   = "FF-" + str(uuid.uuid4())[:8].upper()
    order_time = datetime.now().strftime("%d %b %Y, %I:%M %p")

    session["last_order"] = {
        "order_id":   order_id,
        "order_time": order_time,
        "customer":   session["user"],
        "items":      dict(cart),
        "subtotal":   subtotal,
        "gst":        gst,
        "total":      total,
    }
    session["cart"] = {}
    return redirect(url_for("bill"))

@app.route("/bill")
@login_required
def bill():
    order = session.get("last_order")
    if not order:
        return redirect(url_for("home"))
    return render_template("bill.html", order=order)

if __name__ == "__main__":
    app.run(debug=True)
