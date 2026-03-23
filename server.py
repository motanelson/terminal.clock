from flask import Flask, request, redirect
import sqlite3
import hashlib
import secrets

app = Flask(__name__)

DB = "blog.db"

lista1 = [
    "off_topic",
    "operation_system",
    "cosmos_os",
    "assembly",
    "programming",
    "hardware"
]

# ---------- DB ----------
def get_db():
    return sqlite3.connect(DB, timeout=10, check_same_thread=False)


def init_db():
    with get_db() as db:
        c = db.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            password TEXT,
            approved INTEGER DEFAULT 0,
            activation_key TEXT
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            url TEXT,
            message TEXT
        )
        """)


# ---------- UTIL ----------
def sanitize(text):
    return text.replace("<", "").replace(">", "")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def generate_key():
    return secrets.token_hex(16)


# ---------- USERS ----------
def create_user(url, password):
    key = generate_key()

    with get_db() as db:
        c = db.cursor()
        c.execute(
            "INSERT INTO users (url, password, approved, activation_key) VALUES (?, ?, 0, ?)",
            (url, hash_password(password), key)
        )
        user_id = c.lastrowid

    link = f"http://127.0.0.1:5000/activate/{user_id}/{key}"

    with open("approve.txt", "a", encoding="utf-8") as f:
        f.write(f"{url}|||{link}\n")


def check_user(url, password):
    with get_db() as db:
        c = db.cursor()
        c.execute("SELECT password, approved FROM users WHERE url=?", (url,))
        row = c.fetchone()

    if row:
        if row[0] != hash_password(password):
            return "wrong_pass"
        if row[1] == 0:
            return "not_approved"
        return "ok"

    return "not_exist"


# ---------- POSTS ----------
def save_post(category, url, message):
    with get_db() as db:
        c = db.cursor()
        c.execute(
            "INSERT INTO posts (category, url, message) VALUES (?, ?, ?)",
            (category, url, message)
        )


def load_posts(category):
    with get_db() as db:
        c = db.cursor()
        c.execute(
            "SELECT url, message FROM posts WHERE category=? ORDER BY id DESC",
            (category,)
        )
        return c.fetchall()


# ---------- ROUTES ----------

# 🏠 HOME
@app.route("/")
def home():
    html = """
    <html>
    <head>
        <style>
            body { background:black; color:white; font-family:Arial; }
            a { color:#00ffff; display:block; margin:10px 0; }
        </style>
    </head>
    <body>
        <h1>Categorias</h1>
        <a href="/register">➕ Registar novo utilizador</a>
    """

    for cat in lista1:
        html += f'<a href="/{cat}">{cat}</a>'

    html += "</body></html>"
    return html


# 📝 REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""

    if request.method == "POST":
        url = sanitize(request.form.get("url", ""))
        password = request.form.get("password", "")

        if url and password:
            try:
                create_user(url, password)
                msg = "✅ Registado! Aguarda aprovação."
            except:
                msg = "❌ Utilizador já existe"

    return f"""
    <html>
    <body style="background:black;color:white;font-family:Arial;">
        <a href="/">⬅ Voltar</a>
        <h2>Registar</h2>

        <form method="POST">
            URL:<br>
            <input name="url" required><br>
            Password:<br>
            <input type="password" name="password" required><br>
            <button>Registar</button>
        </form>

        <p>{msg}</p>
    </body>
    </html>
    """


# 🔗 ACTIVATE
@app.route("/activate/<int:user_id>/<key>")
def activate(user_id, key):
    with get_db() as db:
        c = db.cursor()
        c.execute("SELECT activation_key FROM users WHERE id=?", (user_id,))
        row = c.fetchone()

        if row and row[0] == key:
            c.execute("UPDATE users SET approved=1 WHERE id=?", (user_id,))
            db.commit()
            return "✅ Conta ativada com sucesso!"

    return "❌ Link inválido"


# 📄 CATEGORY
@app.route("/<category>", methods=["GET", "POST"])
def category_page(category):
    if category not in lista1:
        return "Categoria inválida", 404

    error = ""

    if request.method == "POST":
        url = sanitize(request.form.get("url", ""))
        message = sanitize(request.form.get("message", ""))
        password = request.form.get("password", "")

        if url and message and password:
            result = check_user(url, password)

            if result == "ok":
                save_post(category, url, message)
                return redirect(f"/{category}")

            elif result == "wrong_pass":
                error = "❌ Password errada!"

            elif result == "not_approved":
                error = "⏳ Conta ainda não ativada!"

            elif result == "not_exist":
                error = "❌ Utilizador não existe! Regista-te primeiro."

    posts = load_posts(category)

    html = f"""
    <html>
    <head>
        <style>
            body {{ background:black; color:white; font-family:Arial; }}
            textarea, input {{
                width:100%;
                background:#111;
                color:white;
                border:1px solid #555;
                padding:10px;
                margin-top:5px;
            }}
            button {{
                margin-top:10px;
                padding:10px;
                background:#333;
                color:white;
                border:none;
            }}
            hr {{ border:1px solid #444; }}
            a {{ color:#00ffff; }}
        </style>
    </head>
    <body>

        <a href="/">⬅ Voltar</a>

        <h2>{category}</h2>

        <form method="POST">
            <label>Endereço (URL):</label>
            <input type="text" name="url" required>

            <label>Password:</label>
            <input type="password" name="password" required>

            <label>Mensagem:</label>
            <textarea name="message" rows="4" required></textarea>

            <button type="submit">Submit</button>
        </form>

        <p style="color:red;">{error}</p>

        <hr>
        <h2>Mensagens</h2>
    """

    for url, msg in posts:
        html += f"""
        <div>
            <b>{url}</b><br>
            <p>{msg}</p>
        </div>
        <hr>
        """

    html += "</body></html>"
    return html


# ---------- START ----------
if __name__ == "__main__":
    init_db()
    app.run(debug=True, use_reloader=False)
