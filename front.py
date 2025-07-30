from flask import Flask, render_template, request, send_file
from services.get_recurent_bills import get_all_fixed_costs, clean_df, PERSON_ID
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    csv_ready = False
    error = None
    if request.method == "POST":
        min_date = request.form.get("min_date")
        max_date = request.form.get("max_date")
        try:
            df = get_all_fixed_costs(PERSON_ID, min_date, max_date)
            if not df.empty:
                clean_df(df)  # Génère le CSV
                csv_ready = True
            else:
                error = "Aucun coût fixe trouvé pour cette période."
        except Exception as e:
            error = str(e)
    return render_template("index.html", csv_ready=csv_ready, error=error)

@app.route("/download")
def download():
    csv_path = "./fixed_costs.csv"
    if os.path.exists(csv_path):
        return send_file(csv_path, as_attachment=True)
    return "Fichier CSV non trouvé.", 404

if __name__ == "__main__":
    app.run(debug=True)
