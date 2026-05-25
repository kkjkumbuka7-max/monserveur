from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_data(filters):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    query = """
    SELECT p.code_eleve, p.frais, p.periode, p.montant, p.devise, p.date,
           e.nom, e.postnom, e.prenom, e.section, e.classe, e.option
    FROM paiements p
    JOIN eleves e ON p.code_eleve = e.code
    WHERE 1=1
    """

    params = []

    if filters.get("frais"):
        query += " AND p.frais=?"
        params.append(filters["frais"])

    if filters.get("periode"):
        query += " AND p.periode=?"
        params.append(filters["periode"])

    if filters.get("section"):
        query += " AND e.section=?"
        params.append(filters["section"])

    if filters.get("classe"):
        query += " AND e.classe=?"
        params.append(filters["classe"])

    query += " ORDER BY p.date DESC"

    cursor.execute(query, params)
    data = cursor.fetchall()

    conn.close()
    return data


@app.route("/", methods=["GET", "POST"])
def dashboard():
    filters = {}

    if request.method == "POST":
        filters["frais"] = request.form.get("frais")
        filters["periode"] = request.form.get("periode")
        filters["section"] = request.form.get("section")
        filters["classe"] = request.form.get("classe")

    data = get_data(filters)

    return render_template("dashboard.html", data=data)


if __name__ == "__main__":
    app.run()