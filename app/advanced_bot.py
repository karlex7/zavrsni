import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from app import report

class bot:
    def __init__(self, stop_loss, starting_money, take_profit, buy_amount, selected_range=-1, filename_model=-1, filename_data=-1):
        self.filename_model = filename_model
        self.filename_data = filename_data
        self.stop_loss = float(stop_loss) / 100
        self.starting_money = float(starting_money)
        self.take_profit = float(take_profit) / 100
        self.buy_amout = float(buy_amount) / 100
        self.selected_range = int(selected_range)

        self.btc_bag = 0
        self.money = float(starting_money)
        self.avg_btc_buy = 0
        self.btc_price = 0
        self.buy_times = 0
        self.avg_btc_sell = 0
        self.sell_times = 0
        self.stop_loss_times = 0
        self.temp_usd_buys = 0
        self.temp_time_buys = 0
        self.avg_buy = 0
    
    def run_advanced_strategy(self):
        #filename = "data/models/ann_1D_2.sav"
        loaded_model = pickle.load(open(self.filename_model, 'rb'))
        data = pd.read_csv(self.filename_data)

        # use slider to cut data
        data = data[:self.selected_range]
        
        self.btc_price = data["close"].iloc[-1]
        

        X = preproces_data(data)
        predictions = loaded_model.predict(X)

        advanced_strategy(self, data, predictions)
        return report.report(self.buy_times,self.avg_btc_buy,self.sell_times,self.avg_btc_sell,self.stop_loss_times,self.btc_bag, self.btc_price, self.money, self.starting_money,self.avg_buy)

def preproces_data(data):
    X = data[[ 'X1', 'X2', 'X3_1', 'X3_2', 'X3_1_vol', 'X3_2_vol', 'X4','X4_vol', 'X5_1','X5_2', 'X5_1_vol', 'X5_2_vol',
          'X6', 'X6_vol', 'X7','X7_vol', 'X8', 'X9','X8_vol','X9_vol','X10_1','X10_2','X11_1','X11_2', 'X12', 'X13', 
          'X12_vol', 'X13_vol','X14', 'X15', 'X16','X17', 'X18']].values

    scale= StandardScaler()
    X = scale.fit_transform(X)

    return X


def advanced_strategy(self, data, predictions):
    buy_times = 0
    buy_ranges = 0
    sell_times = 0
    sell_ranges = 0
    print("------ ADVANCED STRATEGY ---------")
    print("STOP LOSS: ", self.stop_loss)
    print("STARTING MONEY: ", self.starting_money)
    print("TAKE PROFIT: ", self.take_profit)
    print("BUY AMOUT: ", self.buy_amout)
    print("RANGE TRADED: ", self.selected_range)
    print("------------------------------------")

    for i in range(0, len(predictions)):
        if check_for_stop_loss(self, data["close"].iloc[i]):
            if(predictions[i] >= 0.9):

                temp_buy = self.buy_amout * self.money # self.starting_money
                
                if self.money > temp_buy:
                    self.temp_time_buys += 1
                    self.temp_usd_buys += data["close"].iloc[i]
                    self.buy_times += 1
                    self.btc_bag += temp_buy/data["close"].iloc[i]
                    self.money -= temp_buy
                    self.avg_btc_buy += data["close"].iloc[i]
                    print("--")
                    print("Bought BTC: ", temp_buy/data["close"].iloc[i])
                    print("BTC bag: ", self.btc_bag)
                    print("Money: ", self.money)

            else:
                if self.temp_usd_buys > 0 and self.temp_time_buys >0 and self.btc_bag > 0:
                    if (self.temp_usd_buys/self.temp_time_buys)*(1+self.take_profit) > data["close"].iloc[i]:
                        self.sell_times += 1

                        
                        print("--")
                        print("Sold USD: ", self.btc_bag * data["close"].iloc[i])
                        print("BTC bag: ", self.btc_bag)
                        print("Money before: ", self.money)
                        self.money += self.btc_bag * data["close"].iloc[i]
                        print("Money after: ", self.money)
                        self.btc_bag = 0
                        self.temp_time_buys = 0 
                        self.temp_usd_buys = 0
                        self.avg_btc_sell += data["close"].iloc[i]
        self.avg_buy += data["close"].iloc[i]
    self.avg_btc_buy = self.avg_btc_buy / self.buy_times
    self.avg_buy = round(self.avg_buy / len(data))
    self.avg_btc_sell = round(self.avg_btc_sell / self.sell_times)

    print("------ DONE ---------")
    print("----- BUYS ------")
    print("Buy times: ", self.buy_times)
    print("Avg buy price: ", self.avg_btc_buy)
    #print("Avg buy: ", buy_ranges / buy_times)
    print("----- SELLS ------")
    print("Sell times: ", self.sell_times)
    print("Sell ranges: ", self.avg_btc_sell)
    print("----- STOP LOSS -----")
    print("Stop loss times: ", self.stop_loss_times)
    #print("Avg sell: ", sell_ranges / sell_times)
    print("-------------------------")
    print("Money: ", self.money)
    print("BTC BAG: ", self.btc_bag)
    print("BTC price: ",data["close"].iloc[-1])
    print("BTC bag USD value: ", self.btc_bag*data["close"].iloc[-1])
    
def check_for_stop_loss(self, current_price):
    if self.btc_bag > 0 and self.temp_time_buys > 0 and self.temp_usd_buys > 0:
        temp = self.temp_usd_buys / self.temp_time_buys # avg buy price
        if temp < current_price * (1 - self.stop_loss):
            print("---------------------------------------")
            print("             STOP LOSSS")
            print("BTC bag: ", self.btc_bag)
            print("Money: ", self.money)
            print("Current BTC price: ", current_price)
            # stopp loss trigger
            self.money += self.btc_bag * current_price
            print("Money after stop loss: ", self.money)
            self.btc_bag = 0
            self.stop_loss_times += 1
            return False
    return True