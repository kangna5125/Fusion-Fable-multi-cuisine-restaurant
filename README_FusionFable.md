# 🍽️ Fusion Fable — Multi-Cuisine Restaurant Management System

> *Because waiting in line is so last century.*

---

## 💡 Why We Built This

Picture this: it's a Friday evening, you and your friends want to grab dinner, and you already know which restaurant you're going to. But when you get there — the queue is 40 minutes long. You're standing, hungry, waiting just to place an order.

**Fusion Fable was built to fix exactly that.**

We wanted a system where guests can browse the full menu, choose their dishes, and place an order before they even leave the house. No awkward menu-reading under pressure, no shouting over the waiter, no "what did you order again?" when the bill arrives. And for the introverts among us — no social anxiety at the counter either.

Beyond the customer experience, restaurant staff benefit too: orders are cleaner, bills are auto-generated with GST, and the confusion of taking verbal orders vanishes entirely.

It started as a university project, but the problem it solves is real — and anyone who has waited 30 minutes just to tell someone what they want to eat knows it.

---

## ✨ Features

- **Multi-cuisine menu** — Explore Indian (Veg & Non-Veg), Chinese, Italian, and Mexican dishes, all in one place
- **Cuisine-first navigation** — Choose your cuisine, then browse Veg or Non-Veg options within it
- **User authentication** — Sign up, log in, and log out with Flask session management
- **Smart cart system** — Add items with custom quantities, update or remove, see live subtotal
- **Order placement** — Seamless session-based checkout flow
- **Auto bill generation** — Itemized receipt with subtotal, 5% GST, grand total, and a unique order ID
- **Print bill** — Browser print support so your receipt is always a click away

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Frontend | HTML5, CSS3 (custom, no framework) |
| Templating | Jinja2 (via Flask) |
| Auth & Cart | Flask Sessions |
| User Store | JSON file (`users.json`) |

---

## 📁 Project Structure

```
Fusion_Fable/
├── app.py                    # Main Flask app — routes, full menu data, cart & order logic
├── requirements.txt
├── .gitignore
├── templates/
│   ├── index.html            # Home / landing page
│   ├── starters.html         # Starters category (Veg / Non-Veg)
│   ├── choose_cuisine.html   # Cuisine selection page (Indian / Chinese / Italian / Mexican)
│   ├── cuisine_detail.html   # Per-cuisine page with Veg / Non-Veg options
│   ├── menu_page.html        # Shared dynamic template for all dish listings
│   ├── login.html
│   ├── signup.html
│   ├── cart.html             # Cart with live quantity controls
│   └── bill.html             # Order confirmation and itemized bill
└── static/
    ├── auth.css
    ├── menu_page.css
    ├── cart.css
    ├── bill.css
    ├── static.css            # Home page styles
    └── [food images]         # .jpg / .png dish images
```

---

## 🚀 Setup & Run

**1. Clone the repo**
```bash
git clone https://github.com/<your-username>/fusion-fable.git
cd fusion-fable
```

**2. Create a virtual environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
python app.py
```

Open your browser at: **http://127.0.0.1:5000**

---

## 🧭 How It Works

1. Visit the home page and choose between **Starters**, **Main Course**, or **Desserts**
2. For Main Course — pick your **cuisine** first (Indian, Chinese, Italian, Mexican), then choose Veg or Non-Veg
3. **Sign up** or **log in** to start ordering
4. Add dishes to your cart with a custom quantity
5. Review your cart — update quantities, remove items, see the live total with GST
6. Click **Place Order** — a unique bill is generated instantly
7. Optionally **print the bill** directly from the browser

---

## 🍴 Menu Highlights

| Cuisine | Veg | Non-Veg |
|---|---|---|
| 🇮🇳 Indian | Paneer Butter Masala, Palak Paneer, Kashmiri Pulao... | Chicken Tikka Masala, Mutton Rogan Josh, Prawn Malai Curry... |
| 🥢 Chinese | Veg Hakka Noodle, Veg Fried Rice, Paneer Manchurian... | Schezwan Chicken, Chicken Manchurian, Chilly Chicken... |
| 🍕 Italian | Mushroom Risotto, Margherita Pizza, Fettuccine Alfredo... | Chicken Parmesan, Osso Buco, Prawn Linguine... |
| 🌮 Mexican | Veg Tacos, Quesadilla, Enchiladas, Guacamole & Nachos... | Chicken Burrito, Shrimp Fajitas, Carnitas Taco Bowl... |

---

## 📝 Notes

- User data is stored locally in `users.json` (auto-created on first signup; excluded from Git via `.gitignore`)
- Passwords are stored in plaintext — this is an academic project. In production, use `werkzeug.security.generate_password_hash`
- No database required — all state is handled via Flask sessions and a local JSON file

---

*Built as part of B.Tech CSE coursework at Bennett University, Greater Noida.*
