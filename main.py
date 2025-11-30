import requests
from flask import Flask
from flask import render_template
from datetime import date

# Start flask webserver with:
# flask --app main run --debug

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
        f"https://www.elprisetjustnu.se/api/v1/prices/{YEAR}/{MONTH}-{today}_{PRISKLASS}.json"
    )
    elpris_json_tomorrow = requests.get(
        f"https://www.elprisetjustnu.se/api/v1/prices/{YEAR}/{MONTH}-{tomorrow}_{PRISKLASS}.json"
    )
    # jlprint(elpris_json.json())
    priser = elpris_json.json()
    priser_tomorrow = elpris_json_tomorrow.json()
    # for pris in priser:
    #    print(
    #        f"Tid: {pris['time_start'][11:16]} SEK_per_kWh: {pris['SEK_per_kWh']:.3f}"
    #    )
    prices = [round(row["SEK_per_kWh"], 2) for row in priser]
    prices_tomorrow = [round(row["SEK_per_kWh"], 2) for row in priser_tomorrow]
    times = [row["time_start"][11:17] for row in priser]  # transformera tabell

    moving_average_4 = moving_average(4, prices)
    moving_average_8 = moving_average(8, prices)
    print(elpris_json.status_code)  # skapa graf
    # skapa mail med html format som innehåller graf och tabell över elpriset.
    return render_template(
        "prices.html",
        prices=prices,
        prices_tomorrow=prices_tomorrow,
        moving_average_4=moving_average_4,
        moving_average_8=moving_average_8,
        times=times,
    )


def moving_average(samples, price_info):
    moving_average = []

    price_points = len(price_info)
    # print(price_points)
    i = 0
    while i < price_points:
        x = 0
        quater_price = 0
        while x < samples:
            try:
                quater_price += price_info[i + x]
                x += 1
            except IndexError:
                break
        moving_average.append(round(quater_price / samples, 2))
        i += 1
    return moving_average
