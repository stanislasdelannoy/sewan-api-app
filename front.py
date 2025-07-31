from flask import Flask, render_template, request, send_file
from services.get_recurent_bills import get_all_fixed_costs, clean_df, PERSON_ID
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    csv_ready = False
    error = None
    if request.method == "POST":
        min_year = request.form.get("min_year")
        min_month = request.form.get("min_month")
        min_day = request.form.get("min_day")
        max_year = request.form.get("max_year")
        max_month = request.form.get("max_month")
        max_day = request.form.get("max_day")

        min_date = f"{min_year}-{min_month}-{min_day}"
        if max_year and max_month and max_day:
            max_date = f"{max_year}-{max_month}-{max_day}"
        else:
            max_date = ""
        try:
            df = get_all_fixed_costs(PERSON_ID, min_date)
            if not df.empty:
                clean_df(df, min_date, max_date)  # Génère le CSV
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
