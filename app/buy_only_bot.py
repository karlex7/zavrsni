import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from app import report

class bot:
    def __init__(self, selected_range=-1, buy_amout=-1, filename_model=-1, filename_data=-1):
        self.filename_model = filename_model
        self.filename_data = filename_data
        self.selected_range = int(selected_range)
        self.buy_amount = float(buy_amout)

        self.money = 0
        self.money_spent = 0
        self.btc_bag = 0
        self.btc_price = 0
        self.avg_btc_buy = 0
        self.buy_times = 0
        self.avg_btc_sell = 0
        self.sell_times = 0
        self.stop_loss_times = 0
        self.temp_usd_buys = 0
        self.temp_time_buys = 0
        self.avg_buy = 0


    def run_auto_buy_only_strategy(self):
        #filename = "data/models/ann_1D_2.sav"
        loaded_model = pickle.load(open(self.filename_model, 'rb'))
        data = pd.read_csv(self.filename_data)

        print("----------------------------------")
        print("SELECTED RANGE: ", self.selected_range)
        print("----------------------------------")

        # use slider to cut data
        data = data[:self.selected_range]

        self.btc_price = data["close"].iloc[-1]

        X = preproces_data(data)
        predictions = loaded_model.predict(X)

        
        auto_buy_strategy(self, data, predictions)
        return report.report(self.buy_times,self.avg_btc_buy,self.sell_times,self.avg_btc_sell,self.stop_loss_times,self.btc_bag, self.btc_price, self.money, 0, self.avg_buy)
        
        
def preproces_data(data):
    X = data[[ 'X1', 'X2', 'X3_1', 'X3_2', 'X3_1_vol', 'X3_2_vol', 'X4','X4_vol', 'X5_1','X5_2', 'X5_1_vol', 'X5_2_vol',
          'X6', 'X6_vol', 'X7','X7_vol', 'X8', 'X9','X8_vol','X9_vol','X10_1','X10_2','X11_1','X11_2', 'X12', 'X13', 
          'X12_vol', 'X13_vol','X14', 'X15', 'X16','X17', 'X18']].values
    scale= StandardScaler()
    X = scale.fit_transform(X)
    return X

def auto_buy_strategy(self, data, predictions):
        for i in range(0, len(predictions)):
                if(predictions[i] >= 0.9):
                    self.buy_times += 1
                    temp_buy = self.buy_amount / data["close"].iloc[i]
                    self.btc_bag += temp_buy
                    self.money_spent += self.buy_amount #data["close"].iloc[i]
                    self.money -= self.buy_amount
                    self.avg_btc_buy += data["close"].iloc[i]
                self.avg_buy += data["close"].iloc[i]
        self.avg_btc_buy = self.avg_btc_buy / self.buy_times
        self.avg_buy = round(self.avg_buy / len(data))
        print("__________ avg buy: ", self.avg_buy)
        print("------ DONE ---------")
        print("----- BUYS ------")
        print("Buy times: ", self.buy_times)
        print("Avg buy price: ", self.money_spent / self.btc_bag)
        print("Money spent on buy: ", self.money_spent)
        print("-------------------------")
        print("BTC BAG: ", self.btc_bag)
        print("BTC price: ",data["close"].iloc[-1])
        print("BTC bag USD value: ", self.btc_bag*data["close"].iloc[-1])
        print("Profit precentage: ", round((self.btc_bag*data["close"].iloc[-1])/self.money_spent * 100), "%")