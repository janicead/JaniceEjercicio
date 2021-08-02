import json

import requests
from flask import Flask, make_response, Response

app = Flask(__name__)

@app.route("/merchants")
def shipping_merchants():
    data = _get_shipping_options()

    if _check_todos_costos_iguales(data):
        data["shipping_options"] = sorted(data["shipping_options"], key=lambda k: k['estimated_days']) ##aca seria ordenar por estimated_days
    else:
        data["shipping_options"] = sorted(data["shipping_options"], key=lambda k: k['cost']) ## aca seria ordenar por costos

    return Response(json.dumps(data["shipping_options"]), 200, headers={'Content-Type': 'application/json'}) #esto retorna el json que puede ser la lsita vacia o con los datos


def _check_todos_costos_iguales(data):
    for d in data["shipping_options"]:
        if d["cost"] is not data["shipping_options"][0]["cost"]:
            return False
    return True


def _sort_data(data, element): # Esto ordenaria el json por lo que desee
    try:
        return int(data["shipping_merchants"][element])
    except KeyError:
        return 0


def _get_shipping_options():
    URL = "https://shipping-options-api.herokuapp.com/v1/shipping_options/"
    data_shipping = requests.get(url=URL)
    return data_shipping.json()


if __name__ == "__main__":
    app.run()