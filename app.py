from flask import Flask, request, jsonify, render_template
import psycopg2
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")   # ← 前端 index.html

# 連接資料庫（用環境變數）
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "dpg-d2i8ijemcj7s73e3s8dg-a.oregon-postgres.render.com"),
        database=os.getenv("DB_NAME", "ms_data"),
        user=os.getenv("DB_USER", "ms_data_user"),
        password=os.getenv("DB_PASS", "CsRpjfAi4YGkIy2PVP8IUSXOnYXORTH2")
    )
    return conn

@app.route('/add', methods=['POST'])
def add_item():
    data = request.json
    name = data.get('name')
    category = data.get('category')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (name, category) VALUES (%s, %s)", (name, category))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/search', methods=['GET'])
def search_items():
    category = request.args.get('category')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, category FROM items WHERE category = %s", (category,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(rows)

@app.route('/all', methods=['GET'])
def get_all_items():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, category FROM items")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)


if __name__ == "__main__":
    app.run(debug=True)
