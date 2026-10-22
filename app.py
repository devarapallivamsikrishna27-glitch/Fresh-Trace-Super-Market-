from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import sqlite3, json, os

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("FRESHTRACE_DB", BASE_DIR / "freshtrace.db"))
app = Flask(__name__, static_folder="static", static_url_path="/static")

DEFAULT_STATE = {
    "products": [
        {"id":1,"name":"Amul Milk 1L","category":"Dairy","sku":"FT-1001","price":28,"stock":50,"expiry":"2026-10-23","image":"🥛","sold":120,"cost":23,"reorder":10},
        {"id":2,"name":"Britannia Bread","category":"Bakery","sku":"FT-1002","price":40,"stock":30,"expiry":"2026-10-21","image":"🍞","sold":95,"cost":32,"reorder":10},
        {"id":3,"name":"Sunflower Oil 1L","category":"Oil","sku":"FT-1003","price":140,"stock":75,"expiry":"2027-03-20","image":"🧴","sold":80,"cost":120,"reorder":10},
        {"id":4,"name":"Parle Biscuits","category":"Snacks","sku":"FT-1004","price":10,"stock":120,"expiry":"2027-05-15","image":"🍪","sold":65,"cost":7,"reorder":10},
        {"id":5,"name":"Surf Excel 1kg","category":"Home Care","sku":"FT-1005","price":120,"stock":40,"expiry":"2027-06-10","image":"🧼","sold":50,"cost":99,"reorder":10},
        {"id":6,"name":"Curd 500ml","category":"Dairy","sku":"FT-1006","price":35,"stock":18,"expiry":"2026-10-20","image":"🥣","sold":44,"cost":27,"reorder":10},
        {"id":7,"name":"Rice 5kg","category":"Staples","sku":"FT-1007","price":350,"stock":40,"expiry":"2027-10-20","image":"🍚","sold":32,"cost":310,"reorder":10},
        {"id":8,"name":"Bananas 1kg","category":"Produce","sku":"FT-1008","price":55,"stock":12,"expiry":"2026-10-22","image":"🍌","sold":27,"cost":35,"reorder":10}
    ],
    "bills": [
        {"id":"FT-000148","time":"11:42 AM","items":4,"payment":"Cash","amount":548,"status":"Paid"},
        {"id":"FT-000147","time":"11:35 AM","items":7,"payment":"UPI","amount":1280,"status":"Paid"},
        {"id":"FT-000146","time":"11:18 AM","items":2,"payment":"Cash","amount":168,"status":"Paid"},
        {"id":"FT-000145","time":"10:56 AM","items":5,"payment":"Card","amount":735,"status":"Paid"},
        {"id":"FT-000144","time":"10:42 AM","items":3,"payment":"UPI","amount":420,"status":"Paid"}
    ], "purchases": [], "expenses": []
}

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect_db() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS app_state (id INTEGER PRIMARY KEY CHECK (id = 1), payload TEXT NOT NULL, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")
        row = conn.execute("SELECT id FROM app_state WHERE id=1").fetchone()
        if row is None:
            conn.execute("INSERT INTO app_state (id, payload) VALUES (1, ?)", (json.dumps(DEFAULT_STATE, ensure_ascii=False),))

@app.get("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")

@app.get("/api/health")
def health():
    return jsonify({"ok": True, "service": "FreshTrace API"})

@app.get("/api/state")
def get_state():
    with connect_db() as conn:
        row = conn.execute("SELECT payload, updated_at FROM app_state WHERE id=1").fetchone()
    return jsonify({"state": json.loads(row["payload"]), "updated_at": row["updated_at"]})

@app.put("/api/state")
def save_state():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Expected a JSON object."}), 400
    # Keep the API limited to the application collections used by this prototype.
    clean = {key: data.get(key, []) for key in ("products", "bills", "purchases", "expenses")}
    if not isinstance(clean["products"], list) or not isinstance(clean["bills"], list):
        return jsonify({"error": "Products and bills must be lists."}), 400
    with connect_db() as conn:
        conn.execute("UPDATE app_state SET payload=?, updated_at=CURRENT_TIMESTAMP WHERE id=1", (json.dumps(clean, ensure_ascii=False),))
    return jsonify({"ok": True})

@app.get("/api/products")
def products():
    with connect_db() as conn:
        row = conn.execute("SELECT payload FROM app_state WHERE id=1").fetchone()
    return jsonify(json.loads(row["payload"]).get("products", []))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)
