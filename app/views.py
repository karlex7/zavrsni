from crypt import methods
from os import sep
from time import time
from app import app
from flask import render_template, request, redirect
import pandas as pd
from pathlib import Path

from app import trading_bot, advanced_bot, buy_only_bot, infinite_bot, report




@app.route("/") # 24h
@app.route("/index")
def index():
    data = pd.read_csv("data/Bitfinex_BTCUSD_d\.csv")
    #data.sort_values(by = ['unix'], inplace = True)

    data_close = data["close"].values
    data_close = data_close.tolist()

    data_date = data["unix"].values
    data_date = data_date.tolist()

    data_count_max = len(data)

    return render_template("index.html", data_close=data_close, data_date=data_date, data_count_max=data_count_max)

@app.route("/4h")
def index_4():
    data = pd.read_csv("data/data_4h_coinbase_final_test.csv")
    #data.sort_values(by = ['unix'], inplace = True)

    data_close = data["close"].values
    data_close = data_close.tolist()

    data_date = data["date"].values
    data_date = data_date.tolist()
    data_count_max = len(data)

    return render_template("index-4h.html", data_close=data_close, data_date=data_date, data_count_max=data_count_max)

@app.route("/1h")
def index_1():
    data = pd.read_csv("data/data_1h_binance_final_test.csv")
    #data.sort_values(by = ['unix'], inplace = True)

    data_close = data["close"].values
    data_close = data_close.tolist()

    data_date = data["date"].values
    data_date = data_date.tolist()

    data_count_max = len(data)

    return render_template("index-1h.html", data_close=data_close, data_date=data_date, data_count_max=data_count_max)


@app.route("/predict-advanced", methods=["POST"])
def predict_advanced():
    if request.method == "POST":
        req = request.form
        stop_loss = req["stop-loss"]
        starting_money = req["starting-money"]
        take_profit = req["take-profit"]
        buy_amout = req["buy-amout"]
        time_frame = req["timeframe"]
        selected_data_number = req["selected-data-number1"]
        filename_model = model_choser(time_frame)
        filename_data = data_choser(time_frame)
    

        bot = advanced_bot.bot(stop_loss, starting_money, take_profit, buy_amout,selected_data_number, filename_model, filename_data)
        bot_report= bot.run_advanced_strategy()

    return render_template("predict.html", bot_report=bot_report)

@app.route("/predict-auto-buy-sell", methods=["POST"])
def predict_auto_buy_sell():
    if request.method == "POST":
        req = request.form
        starting_money = req["starting-money-buy-sell"]
        buy_amout = req["buy-amout-buy-sell"]
        selected_data_number = req["selected-data-number2"]
        time_frame = req["timeframe"]
        filename_model = model_choser(time_frame)
        filename_data = data_choser(time_frame)

        bot = trading_bot.bot(starting_money, buy_amout,selected_data_number, filename_model, filename_data)
        
        bot_report= bot.run_auto_buy_sell_strategy()

    return render_template("predict.html", bot_report=bot_report)

@app.route("/predict-infinity", methods=["POST"])
def predict_auto_buy():
    if request.method == "POST":
        req = request.form
        selected_data_number = req["selected-data-number4"]
        time_frame = req["timeframe"]
        filename_model = model_choser(time_frame)
        filename_data = data_choser(time_frame)

        bot = infinite_bot.bot(selected_data_number, filename_model, filename_data)
        bot_report= bot.run_auto_buy_sell_strategy()
    return render_template("predict.html", bot_report=bot_report)

@app.route("/predict-buy-only", methods=["POST"])
def predict_infinity_buy():
    if request.method == "POST":
        req = request.form
        selected_data_number = req["selected-data-number3"]
        time_frame = req["timeframe"]
        buy_amout = req["buy-amount"]
        filename_model = model_choser(time_frame)
        filename_data = data_choser(time_frame)
        print("----------------------------------")
        print("SELECTED RANGE: ", selected_data_number)
        print("----------------------------------")
        

        bot = buy_only_bot.bot(selected_data_number, buy_amout ,filename_model, filename_data)
        bot_report= bot.run_auto_buy_only_strategy()
        print("_______________ avg buyyy: ", bot_report.avg_buy)
    return render_template("predict.html", bot_report=bot_report)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/features")
def features():
    return render_template("features.html")

def model_choser(time_frame):
    print("Time frame: ", time_frame)
    if time_frame == "24":
        return "data/models/ann_1D.sav"
    elif time_frame == "4":
        return "data/models/ann_4h.sav"
    else:
        return "data/models/ann_1h.sav"

def data_choser(time_frame):
    print("Time frame: ", time_frame)
    if time_frame == "24":
        return "data/Bitfinex_BTCUSD_d\.csv"
    elif time_frame == "4":
        return "data/data_4h_coinbase_final_test.csv"
    else:
        return "data/data_1h_binance_final_test.csv"


