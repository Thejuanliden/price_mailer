import requests
from flask import Flask
from flask import render_template
from datetime import date


app = Flask(__name__)
# datetime
# json
# requests
#
# hämta datum ,


# Hämta json med api från elpriset.nu
# elpris_json = "skriv ut elpriset"


@app.route("/prices")
def price_table():
    YEAR = str(2025)
    MONTH = str(11)
    print(date.today())
    print(type(date.today()))
    DAG = str("06")
    d = date.today()
    today = d.strftime("%d")
    print(f"today:{today}")
    tomorrow = str(int(today) + 1)
    print(f"tomorrow:{tomorrow}")
    PRISKLASS = str("SE3")

    elpris_json = requests.get(
        f"https://www.elprisetjustnu.se/api/v1/prices/{YEAR}/{MONTH}-{DAG}_{PRISKLASS}.json"
    )
    # jlprint(elpris_json.json())
    priser = elpris_json.json()
    for pris in priser:
        print(
            f"Tid: {pris['time_start'][11:16]} SEK_per_kWh: {pris['SEK_per_kWh']:.3f}"
        )
    # transformera tabell
    print(elpris_json.status_code)  # skapa graf
    # skapa mail med html format som innehåller graf och tabell över elpriset.
    return render_template("prices.html", priser=priser)
