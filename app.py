from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import sqlite3
import os

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "gise_verileri.db")
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM gise_verileri", conn)
    conn.close()
    df["TARİH"] = pd.to_datetime(df["TARİH"], errors='coerce')
    return df

data = load_data()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    regions = sorted(data["BÖLGE MÜDÜRLÜĞÜ"].dropna().unique())
    classes = ["1.SINIF", "2.SINIF", "3.SINIF", "4.SINIF", "5.SINIF", "6.SINIF"]
    selected_region = request.form.get("region")
    selected_tollbooths = request.form.getlist("tollbooth")
    selected_classes = request.form.getlist("class")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    total_data = None

    # Seçili bölgeye göre gişe listesini getir
    tollbooths = sorted(data[data["BÖLGE MÜDÜRLÜĞÜ"] == selected_region]["GİŞE ADI"].unique()) if selected_region else []

    if request.method == 'POST' and request.form.get("action") == "search":
        if not (selected_region and selected_tollbooths and selected_classes and start_date and end_date):
            result = "Lütfen tüm alanları doldurun."
        else:
            try:
                start_date_obj = pd.to_datetime(start_date)
                end_date_obj = pd.to_datetime(end_date)

                if start_date_obj > pd.to_datetime('today'):
                    result = "Başlangıç tarihi bugünden sonra olamaz."
                elif end_date_obj < start_date_obj:
                    result = "Bitiş tarihi başlangıç tarihinden önce olamaz."
                elif end_date_obj > pd.to_datetime('today'):
                    result = "Bitiş tarihi bugünden sonra olamaz."
                else:
                    filtered_data = data[
                        (data["BÖLGE MÜDÜRLÜĞÜ"] == selected_region) &
                        (data["GİŞE ADI"].isin(selected_tollbooths)) &
                        (data["TARİH"] >= start_date_obj) &
                        (data["TARİH"] <= end_date_obj)
                    ]

                    if filtered_data.empty:
                        result = "Seçilen kriterlere uygun veri bulunamadı."
                    else:
                        total_data = {cls: "{:,}".format(int(filtered_data[cls].sum())) for cls in selected_classes}
            except Exception as e:
                result = f"Bir hata oluştu: {str(e)}"

    if request.form.get("action") == "reset":
        return redirect(url_for('index'))

    return render_template("index.html",
                           regions=regions,
                           classes=classes,
                           tollbooths=tollbooths,
                           result=result,
                           total_data=total_data,
                           selected_region=selected_region,
                           selected_tollbooths=selected_tollbooths,
                           selected_classes=selected_classes,
                           start_date=start_date,
                           end_date=end_date)

@app.route('/get_tollbooths', methods=['POST'])
def get_tollbooths():
    selected_region = request.json.get("region")
    tollbooths = sorted(data[data["BÖLGE MÜDÜRLÜĞÜ"] == selected_region]["GİŞE ADI"].unique()) if selected_region else []
    return jsonify({"tollbooths": tollbooths})

if __name__ == '__main__':
    app.run(debug=True)
