from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect("expenses.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/expenses", methods=["GET"])
def get_expenses():
        conn = get_db_connection()
        expenses = conn.execute("SELECT * FROM expenses").fetchall()
        conn.close()
        return jsonify([dict(row) for row in expenses])


@app.route("/add", methods=["POST"])
def add_expense():
    data = request.json 
    if not data:
        return jsonify({"error": "No data sent"}), 400

    if not data.get("amount") or not data.get("category") or not data.get("date"):
        return jsonify({"error": "amount, category, and date are required"}), 400

    try:
        float(data["amount"])
    except:
        return jsonify({"error": "Amount must be a number"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()   # ✅ THIS WAS MISSING

    cursor.execute(
        "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
        (data["amount"], data["category"], data["date"], data.get("note"))
    )
    conn.commit()

    new_expense = {
        "id": cursor.lastrowid,
        "amount": data["amount"],
        "category": data["category"],
        "date": data["date"],
        "note": data.get("note")
    }

    conn.close()
    return jsonify(new_expense), 201



@app.route("/summary/category", methods=["GET"])
def category_summary():
    conn = get_db_connection()
    result = conn.execute(
        "SELECT category, SUM(amount) as total FROM expenses GROUP BY category"
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in result])


@app.route("/summary/monthly", methods=["GET"])
def monthly_summary():
    conn = get_db_connection()
    result = conn.execute(
        "SELECT strftime('%Y-%m', date) as month, SUM(amount) as total FROM expenses GROUP BY month"
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in result])

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_expense(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Expense deleted successfully"})

@app.route("/update/<int:id>", methods=["PUT"])
def update_expense(id):
    data = request.json
    conn = get_db_connection()
    conn.execute(
        "UPDATE expenses SET amount = ?, category = ?, date = ?, note = ? WHERE id = ?",
        (data["amount"], data["category"], data["date"], data["note"], id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Expense updated successfully"})


if __name__ == "__main__":
    app.run(debug=True)
