import requests
from bottle import request, route, run
from datetime import datetime, timedelta


@route('/currency')
def currency_rate():
    param = request.query.get('param')
    URL = "https://bank.gov.ua/NBU_Exchange/exchange_site?json"

    # GET today
    response_today = requests.get(URL)
    if response_today.status_code != 200:
        return {"error": "Data from NBU API isn't received"}, 500
    all_today = response_today.json()

    rate_today = next((item for item in all_today if item.get("cc") == "USD"), None)

    if param == 'today':
        if rate_today:
            return {"Date": rate_today["exchangedate"], "Rate": rate_today["rate"]}
        else:
            return {"error": "There's no USD rate for today. Try to use request 'yesterday' "}, 404

    elif param == 'yesterday':
        # GET yesterday
        yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        response_yesterday = requests.get(f"https://bank.gov.ua/NBU_Exchange/exchange_site?date={yesterday_date}&json")

        if response_yesterday.status_code != 200:
            return {"error": "Data from NBU API isn't received"}, 500

        all_yesterday = response_yesterday.json()
        rate_yesterday = next((item for item in all_yesterday if item.get("cc") == "USD"), None)

        if not rate_yesterday:
            # Так як на вихідні та свята курс не оновлюється, якщо немає даних за вчора, перевіряємо за позавчора
            dbyesterday = (datetime.now() - timedelta(days=2)).strftime('%Y%m%d')
            response_dbyesterday = requests.get(
                f"https://bank.gov.ua/NBU_Exchange/exchange_site?date={dbyesterday}&json")

            if response_dbyesterday.status_code != 200:
                return {"error": "Data from NBU API isn't received"}, 500

            all_dbyesterday = response_dbyesterday.json()
            rate_dbyesterday = next((item for item in all_dbyesterday if item.get("cc") == "USD"), None)

            if rate_dbyesterday:
                return {"There's no USD rate for yesterday. Here is rate for the day before yesterday." "Date": rate_dbyesterday["exchangedate"], "Rate": rate_dbyesterday["rate"]}
            else:
                return {"error": "There's no USD rate for the day before yesterday"}, 404

        return {"Date": rate_yesterday["exchangedate"], "Rate": rate_yesterday["rate"]}

    else:
        return {"error": "Unknown request. Use only 'today' or 'yesterday'."}, 400


if __name__ == "__main__":
    run(host='localhost', port=8000)
